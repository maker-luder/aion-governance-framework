from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class ReplayStrategy(str, Enum):
    BREADTH_FIRST = "BREADTH_FIRST"
    DEPTH_FIRST = "DEPTH_FIRST"


@dataclass(frozen=True)
class DiscoveryNode:
    node_id: str
    parent_id: str | None
    action_id: str
    score: int
    execution_cost: int = 1
    terminal: bool = False

    def __post_init__(self) -> None:
        if not self.node_id:
            raise ValueError("node_id must be non-empty")
        if not self.action_id:
            raise ValueError("action_id must be non-empty")
        if self.execution_cost <= 0:
            raise ValueError("execution_cost must be positive")


@dataclass(frozen=True)
class DiscoveryTree:
    tree_id: str
    nodes: tuple[DiscoveryNode, ...]

    def __post_init__(self) -> None:
        if not self.tree_id:
            raise ValueError("tree_id must be non-empty")
        if not self.nodes:
            raise ValueError("nodes must be non-empty")

        by_id = {node.node_id: node for node in self.nodes}
        if len(by_id) != len(self.nodes):
            raise ValueError("node_id values must be unique")

        roots = [node for node in self.nodes if node.parent_id is None]
        if len(roots) != 1:
            raise ValueError("tree must contain exactly one root")

        terminal_ids = {node.node_id for node in self.nodes if node.terminal}
        for node in self.nodes:
            if node.parent_id is not None and node.parent_id not in by_id:
                raise ValueError(f"missing parent for node {node.node_id}")
            if node.parent_id in terminal_ids:
                raise ValueError("terminal nodes cannot have children")

        root_id = roots[0].node_id
        for node in self.nodes:
            seen: set[str] = set()
            current = node
            while current.parent_id is not None:
                if current.node_id in seen:
                    raise ValueError("tree contains a cycle")
                seen.add(current.node_id)
                current = by_id[current.parent_id]
            if current.node_id != root_id:
                raise ValueError("all nodes must descend from the single root")

    @property
    def root_id(self) -> str:
        return next(node.node_id for node in self.nodes if node.parent_id is None)

    @property
    def history_sha256(self) -> str:
        """Bind replay semantics to the exact ordered discovery-history content.

        Node tuple order is intentionally part of the fingerprint because it defines
        sibling/frontier ordering for deterministic breadth/depth replay. ``tree_id``
        is excluded so labels cannot substitute for content identity.
        """

        payload = [
            {
                "node_id": node.node_id,
                "parent_id": node.parent_id,
                "action_id": node.action_id,
                "score": node.score,
                "execution_cost": node.execution_cost,
                "terminal": node.terminal,
            }
            for node in self.nodes
        ]
        canonical = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def node(self, node_id: str) -> DiscoveryNode:
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        raise KeyError(node_id)

    def children(self, parent_id: str) -> tuple[DiscoveryNode, ...]:
        return tuple(node for node in self.nodes if node.parent_id == parent_id)


@dataclass(frozen=True)
class ReplayPolicy:
    policy_id: str
    strategy: ReplayStrategy
    max_visits: int
    patience: int | None = None

    def __post_init__(self) -> None:
        if not self.policy_id:
            raise ValueError("policy_id must be non-empty")
        if self.max_visits <= 0:
            raise ValueError("max_visits must be positive")
        if self.patience is not None and self.patience <= 0:
            raise ValueError("patience must be positive when supplied")


@dataclass(frozen=True)
class ReplayResult:
    tree_id: str
    history_sha256: str
    policy_id: str
    visited_nodes: tuple[str, ...]
    cumulative_cost: int
    best_score: int
    terminal_reason: str


@dataclass(frozen=True)
class PolicyComparison:
    tree_id: str
    history_sha256: str
    max_visits: int
    results: tuple[ReplayResult, ...]

    def result_for(self, policy_id: str) -> ReplayResult:
        for result in self.results:
            if result.policy_id == policy_id:
                return result
        raise KeyError(policy_id)


def _select_frontier_index(strategy: ReplayStrategy, frontier_size: int) -> int:
    if frontier_size <= 0:
        raise ValueError("frontier_size must be positive")
    if strategy is ReplayStrategy.BREADTH_FIRST:
        return 0
    if strategy is ReplayStrategy.DEPTH_FIRST:
        return frontier_size - 1
    raise ValueError(f"unsupported strategy: {strategy}")


def replay(tree: DiscoveryTree, policy: ReplayPolicy) -> ReplayResult:
    """Replay a policy against already-recorded history without oracle access."""

    frontier: list[str] = [tree.root_id]
    visited: list[str] = []
    cumulative_cost = 0
    best_score: int | None = None
    no_improvement = 0
    terminal_reason = "FRONTIER_EXHAUSTED"

    while frontier and len(visited) < policy.max_visits:
        index = _select_frontier_index(policy.strategy, len(frontier))
        node_id = frontier.pop(index)
        node = tree.node(node_id)

        visited.append(node.node_id)
        cumulative_cost += node.execution_cost

        if best_score is None or node.score > best_score:
            best_score = node.score
            no_improvement = 0
        else:
            no_improvement += 1

        if not node.terminal:
            frontier.extend(child.node_id for child in tree.children(node.node_id))

        if policy.patience is not None and no_improvement >= policy.patience:
            terminal_reason = "PATIENCE_EXHAUSTED"
            break
    else:
        if len(visited) >= policy.max_visits and frontier:
            terminal_reason = "VISIT_BUDGET_EXHAUSTED"

    if best_score is None:
        raise RuntimeError("replay visited no nodes")

    return ReplayResult(
        tree_id=tree.tree_id,
        history_sha256=tree.history_sha256,
        policy_id=policy.policy_id,
        visited_nodes=tuple(visited),
        cumulative_cost=cumulative_cost,
        best_score=best_score,
        terminal_reason=terminal_reason,
    )


def compare_policies(
    tree: DiscoveryTree,
    policies: Iterable[ReplayPolicy],
) -> PolicyComparison:
    policy_tuple = tuple(policies)
    if not policy_tuple:
        raise ValueError("at least one policy is required")

    policy_ids = {policy.policy_id for policy in policy_tuple}
    if len(policy_ids) != len(policy_tuple):
        raise ValueError("policy_id values must be unique")

    visit_budgets = {policy.max_visits for policy in policy_tuple}
    if len(visit_budgets) != 1:
        raise ValueError("compared policies must share max_visits")
    max_visits = next(iter(visit_budgets))

    return PolicyComparison(
        tree_id=tree.tree_id,
        history_sha256=tree.history_sha256,
        max_visits=max_visits,
        results=tuple(replay(tree, policy) for policy in policy_tuple),
    )


def select_on_training_history(comparison: PolicyComparison) -> ReplayResult:
    """Select on one replay history only; held-out generalization is separate."""

    return sorted(
        comparison.results,
        key=lambda result: (
            -result.best_score,
            result.cumulative_cost,
            result.policy_id,
        ),
    )[0]
