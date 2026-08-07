"""Transactional owner-gated repository and minimum public API."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from .database import Database
from .engine import (
    calculate_annual_cycle,
    calculate_four_pillars,
    calculate_luck_cycles,
    calculate_monthly_cycle,
    calculate_natal_profile as derive_natal_profile,
)
from .enums import (
    BindingStatus,
    DayRolloverRule,
    InterpretationStatus,
    LuckDirection,
    MonthBoundaryRule,
    OwnerReviewStatus,
    SolarTimeRule,
    SourceType,
    TimePrecision,
    YearBoundaryRule,
)
from .errors import OwnerGateRequiredError, RepositoryError, ValidationError
from .models import (
    AgentBaziBinding,
    BaziRuleProfile,
    BaziSourceInput,
    CalendarContext,
    CycleFact,
    InterpretationCandidate,
    LuckCycle,
    NatalProfile,
    Pillar,
)
from .serialization import canonical_json
from .integrity import (
    SERIALIZATION_SCHEMA_VERSION,
    materialized_category_counts,
    materialized_facts_hash,
)


class BaziCore:
    def __init__(self, database: Database) -> None:
        self.database = database

    def _audit(
        self,
        connection: Any,
        *,
        audit_stream_id: str,
        occurred_at: str,
        actor_id: str,
        action: str,
        target_type: str,
        target_id: str,
        details: dict[str, Any],
    ) -> None:
        connection.execute(
            """INSERT INTO bazi_audit_events(
               audit_stream_id, occurred_at, actor_id, action,
               target_type, target_id, details_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                audit_stream_id,
                occurred_at,
                actor_id,
                action,
                target_type,
                target_id,
                canonical_json(details),
            ),
        )

    def _record_materialization_snapshot(
        self,
        connection: Any,
        *,
        natal_profile_id: str,
        created_at: str,
    ) -> None:
        version_row = connection.execute(
            """SELECT COALESCE(MAX(materialization_version), 0) + 1
               FROM bazi_materialization_snapshots
               WHERE natal_profile_id=?""",
            (natal_profile_id,),
        ).fetchone()
        version = int(version_row[0])
        connection.execute(
            """INSERT INTO bazi_materialization_snapshots(
               natal_profile_id, materialization_version,
               materialized_facts_hash, serialization_schema_version,
               expected_categories_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?)""",
            (
                natal_profile_id,
                version,
                materialized_facts_hash(connection, natal_profile_id),
                SERIALIZATION_SCHEMA_VERSION,
                canonical_json(
                    materialized_category_counts(connection, natal_profile_id)
                ),
                created_at,
            ),
        )

    def create_rule_profile(self, profile: BaziRuleProfile, *, created_at: str) -> BaziRuleProfile:
        with self.database.transaction() as connection:
            connection.execute(
                """INSERT INTO bazi_rule_profiles(
                   rule_profile_id, version, profile_json, owner_review_status, created_at
                ) VALUES (?, ?, ?, ?, ?)""",
                (
                    profile.rule_profile_id,
                    profile.version,
                    canonical_json(profile),
                    profile.owner_review_status.value,
                    created_at,
                ),
            )
        return profile

    def get_rule_profile(self, rule_profile_id: str) -> BaziRuleProfile | None:
        row = self.database.connection.execute(
            "SELECT profile_json FROM bazi_rule_profiles WHERE rule_profile_id=?",
            (rule_profile_id,),
        ).fetchone()
        if row is None:
            return None
        data = json.loads(row[0])
        return BaziRuleProfile(
            **{
                **data,
                "year_boundary_rule": YearBoundaryRule(data["year_boundary_rule"]),
                "month_boundary_rule": MonthBoundaryRule(data["month_boundary_rule"]),
                "day_rollover_rule": DayRolloverRule(data["day_rollover_rule"]),
                "solar_time_rule": SolarTimeRule(data["solar_time_rule"]),
                "source_references": tuple(data["source_references"]),
                "owner_review_status": OwnerReviewStatus(data["owner_review_status"]),
            }
        )

    def create_source_input(self, source: BaziSourceInput) -> BaziSourceInput:
        if source.time_precision is TimePrecision.UNKNOWN:
            raise ValidationError("unknown birth time cannot be silently calculated")
        with self.database.transaction() as connection:
            connection.execute(
                """INSERT INTO bazi_source_inputs(
                   input_id, local_datetime, timezone_id, utc_offset_at_event,
                   location_name, latitude, longitude, time_precision, source_type,
                   source_reference, owner_confirmation_status, recorded_at,
                   supersedes, audit_stream_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    source.input_id,
                    source.local_datetime,
                    source.timezone_id,
                    source.utc_offset_at_event,
                    source.location_name,
                    source.latitude,
                    source.longitude,
                    source.time_precision.value,
                    source.source_type.value,
                    source.source_reference,
                    source.owner_confirmation_status.value,
                    source.recorded_at,
                    source.supersedes,
                    source.audit_stream_id,
                ),
            )
            self._audit(
                connection,
                audit_stream_id=source.audit_stream_id,
                occurred_at=source.recorded_at,
                actor_id="OWNER",
                action="bazi.source.create",
                target_type="BAZI_SOURCE_INPUT",
                target_id=source.input_id,
                details={"supersedes": source.supersedes},
            )
        return source

    def supersede_source_input(
        self,
        previous_input_id: str,
        replacement: BaziSourceInput,
    ) -> BaziSourceInput:
        if replacement.supersedes != previous_input_id:
            raise ValidationError("replacement must explicitly supersede previous input")
        if self.get_source_input(previous_input_id) is None:
            raise ValidationError("superseded source input does not exist")
        return self.create_source_input(replacement)

    def get_source_input(self, input_id: str) -> BaziSourceInput | None:
        row = self.database.connection.execute(
            "SELECT * FROM bazi_source_inputs WHERE input_id=?",
            (input_id,),
        ).fetchone()
        if row is None:
            return None
        return BaziSourceInput(
            input_id=row["input_id"],
            local_datetime=row["local_datetime"],
            timezone_id=row["timezone_id"],
            utc_offset_at_event=row["utc_offset_at_event"],
            location_name=row["location_name"],
            latitude=row["latitude"],
            longitude=row["longitude"],
            time_precision=TimePrecision(row["time_precision"]),
            source_type=SourceType(row["source_type"]),
            source_reference=row["source_reference"],
            owner_confirmation_status=OwnerReviewStatus(row["owner_confirmation_status"]),
            recorded_at=row["recorded_at"],
            supersedes=row["supersedes"],
            audit_stream_id=row["audit_stream_id"],
        )

    def calculate_natal_profile(
        self,
        input_id: str,
        rule_profile_id: str,
        *,
        calculation_run_id: str,
        natal_profile_id: str,
        generated_at: str,
    ) -> NatalProfile:
        source = self.get_source_input(input_id)
        profile = self.get_rule_profile(rule_profile_id)
        if source is None or profile is None:
            raise ValidationError("source input or rule profile does not exist")
        result = derive_natal_profile(
            source,
            profile,
            calculation_run_id=calculation_run_id,
            natal_profile_id=natal_profile_id,
            generated_at=generated_at,
        )
        with self.database.transaction() as connection:
            connection.execute(
                """INSERT INTO bazi_calculation_runs(
                   calculation_run_id, input_id, rule_profile_id, algorithm_version,
                   ephemeris_version, derivation_hash, generated_at, trace_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    result.calculation_run_id,
                    result.input_id,
                    result.rule_profile_id,
                    result.algorithm_version,
                    result.ephemeris_version,
                    result.derivation_hash,
                    result.generated_at,
                    canonical_json(result.derivation_trace),
                ),
            )
            connection.execute(
                """INSERT INTO bazi_natal_profiles(
                   natal_profile_id, input_id, calculation_run_id, rule_profile_id,
                   derivation_hash, calendar_context_json, generated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    result.natal_profile_id,
                    result.input_id,
                    result.calculation_run_id,
                    result.rule_profile_id,
                    result.derivation_hash,
                    canonical_json(result.calendar_context),
                    result.generated_at,
                ),
            )
            for pillar in result.pillars:
                connection.execute(
                    """INSERT INTO bazi_pillars(
                       natal_profile_id, pillar_name, stem, branch, fact_json
                    ) VALUES (?, ?, ?, ?, ?)""",
                    (
                        result.natal_profile_id,
                        pillar.name,
                        pillar.stem,
                        pillar.branch,
                        canonical_json(pillar),
                    ),
                )
                for index, hidden in enumerate(pillar.hidden_stems):
                    connection.execute(
                        "INSERT INTO bazi_hidden_stems VALUES (?, ?, ?, ?)",
                        (result.natal_profile_id, pillar.name, index, hidden),
                    )
                for index, god in enumerate(pillar.ten_gods):
                    connection.execute(
                        "INSERT INTO bazi_ten_gods VALUES (?, ?, ?, ?)",
                        (result.natal_profile_id, pillar.name, index, god),
                    )
            for index, relation in enumerate(result.relations):
                connection.execute(
                    "INSERT INTO bazi_relations VALUES (?, ?, ?, ?)",
                    (
                        result.natal_profile_id,
                        index,
                        str(relation["type"]),
                        canonical_json(relation),
                    ),
                )
            self._record_materialization_snapshot(
                connection,
                natal_profile_id=result.natal_profile_id,
                created_at=generated_at,
            )
            self._audit(
                connection,
                audit_stream_id=source.audit_stream_id,
                occurred_at=generated_at,
                actor_id="OWNER_APPROVED_ENGINE",
                action="bazi.calculate",
                target_type="BAZI_NATAL_PROFILE",
                target_id=result.natal_profile_id,
                details={"derivation_hash": result.derivation_hash},
            )
        return result

    def get_natal_profile(self, natal_profile_id: str) -> NatalProfile | None:
        row = self.database.connection.execute(
            """SELECT n.*, r.algorithm_version, r.ephemeris_version, r.trace_json
               FROM bazi_natal_profiles n
               JOIN bazi_calculation_runs r
                 ON r.calculation_run_id=n.calculation_run_id
               WHERE n.natal_profile_id=?""",
            (natal_profile_id,),
        ).fetchone()
        if row is None:
            return None
        pillar_rows = self.database.connection.execute(
            "SELECT fact_json FROM bazi_pillars WHERE natal_profile_id=? ORDER BY rowid",
            (natal_profile_id,),
        ).fetchall()
        pillars = tuple(
            Pillar(
                **{
                    **json.loads(item[0]),
                    "hidden_stems": tuple(json.loads(item[0])["hidden_stems"]),
                    "ten_gods": tuple(json.loads(item[0])["ten_gods"]),
                    "void_branches": tuple(json.loads(item[0])["void_branches"]),
                }
            )
            for item in pillar_rows
        )
        relation_rows = self.database.connection.execute(
            "SELECT relation_json FROM bazi_relations WHERE natal_profile_id=? ORDER BY sequence",
            (natal_profile_id,),
        ).fetchall()
        context_data = json.loads(row["calendar_context_json"])
        return NatalProfile(
            natal_profile_id=row["natal_profile_id"],
            input_id=row["input_id"],
            calculation_run_id=row["calculation_run_id"],
            rule_profile_id=row["rule_profile_id"],
            algorithm_version=row["algorithm_version"],
            ephemeris_version=row["ephemeris_version"],
            pillars=pillars,
            relations=tuple(json.loads(item[0]) for item in relation_rows),
            calendar_context=CalendarContext(**context_data),
            derivation_trace=tuple(json.loads(row["trace_json"])),
            derivation_hash=row["derivation_hash"],
            generated_at=row["generated_at"],
        )

    def calculate_four_pillars(
        self,
        source: BaziSourceInput,
        profile: BaziRuleProfile,
    ) -> tuple[Pillar, ...]:
        return calculate_four_pillars(source, profile)[0]

    def calculate_hidden_stems(self, natal_profile_id: str) -> dict[str, tuple[str, ...]]:
        profile = self._required_profile(natal_profile_id)
        return {pillar.name: pillar.hidden_stems for pillar in profile.pillars}

    def calculate_ten_gods(self, natal_profile_id: str) -> dict[str, tuple[str, ...]]:
        profile = self._required_profile(natal_profile_id)
        return {pillar.name: pillar.ten_gods for pillar in profile.pillars}

    def calculate_twelve_stages(self, natal_profile_id: str) -> dict[str, str]:
        profile = self._required_profile(natal_profile_id)
        return {pillar.name: pillar.twelve_stage for pillar in profile.pillars}

    def calculate_relationships(self, natal_profile_id: str) -> tuple[dict[str, Any], ...]:
        return self._required_profile(natal_profile_id).relations

    def calculate_luck_cycles(
        self,
        natal_profile_id: str,
        direction: LuckDirection,
        start_age_years: float,
        *,
        count: int = 8,
    ) -> tuple[LuckCycle, ...]:
        profile = self._required_profile(natal_profile_id)
        cycles = calculate_luck_cycles(profile, direction, start_age_years, count)
        with self.database.transaction() as connection:
            for cycle in cycles:
                connection.execute(
                    """INSERT INTO bazi_luck_cycles(
                       natal_profile_id, sequence, pillar, start_age_years,
                       end_age_years, direction
                    ) VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        natal_profile_id,
                        cycle.sequence,
                        cycle.pillar,
                        cycle.start_age_years,
                        cycle.end_age_years,
                        direction.value,
                    ),
                )
            self._record_materialization_snapshot(
                connection,
                natal_profile_id=natal_profile_id,
                created_at=profile.generated_at,
            )
        return cycles

    def calculate_annual_cycle(self, year: int, rule_profile_id: str) -> CycleFact:
        return calculate_annual_cycle(year, rule_profile_id)

    def calculate_monthly_cycle(self, year: int, month: int, rule_profile_id: str) -> CycleFact:
        return calculate_monthly_cycle(year, month, rule_profile_id)

    def create_interpretation_candidate(
        self,
        candidate: InterpretationCandidate,
        *,
        created_at: str,
        supersedes_interpretation_id: str | None = None,
    ) -> InterpretationCandidate:
        with self.database.transaction() as connection:
            connection.execute(
                """INSERT INTO bazi_interpretation_candidates(
                   interpretation_id, natal_profile_id, rule_profile_id,
                   candidate_json, confidence, owner_review_status, created_at,
                   supersedes_interpretation_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    candidate.interpretation_id,
                    candidate.natal_profile_id,
                    candidate.rule_profile_id,
                    canonical_json(candidate),
                    candidate.confidence,
                    candidate.owner_review_status.value,
                    created_at,
                    supersedes_interpretation_id,
                ),
            )
        return candidate

    def supersede_interpretation_candidate(
        self,
        previous_interpretation_id: str,
        replacement: InterpretationCandidate,
        *,
        created_at: str,
    ) -> InterpretationCandidate:
        previous = self.database.connection.execute(
            "SELECT 1 FROM bazi_interpretation_candidates WHERE interpretation_id=?",
            (previous_interpretation_id,),
        ).fetchone()
        if previous is None:
            raise ValidationError("previous interpretation candidate does not exist")
        return self.create_interpretation_candidate(
            replacement,
            created_at=created_at,
            supersedes_interpretation_id=previous_interpretation_id,
        )

    def bind_agent_to_natal_profile(self, binding: AgentBaziBinding) -> AgentBaziBinding:
        if not binding.approved_by:
            raise OwnerGateRequiredError("agent binding requires approved_by")
        with self.database.transaction() as connection:
            connection.execute(
                """INSERT INTO agent_bazi_bindings(
                   binding_id, agent_id, natal_profile_id, binding_type,
                   approved_by, approved_at, status, audit_stream_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    binding.binding_id,
                    binding.agent_id,
                    binding.natal_profile_id,
                    binding.binding_type,
                    binding.approved_by,
                    binding.approved_at,
                    binding.status.value,
                    binding.audit_stream_id,
                ),
            )
            self._audit(
                connection,
                audit_stream_id=binding.audit_stream_id,
                occurred_at=binding.approved_at,
                actor_id=binding.approved_by,
                action="bazi.binding.create",
                target_type="AGENT_BAZI_BINDING",
                target_id=binding.binding_id,
                details={"runtime_effect": "NONE"},
            )
        return binding

    def get_agent_bazi_binding(self, binding_id: str) -> AgentBaziBinding | None:
        row = self.database.connection.execute(
            "SELECT * FROM agent_bazi_bindings WHERE binding_id=?",
            (binding_id,),
        ).fetchone()
        if row is None:
            return None
        return AgentBaziBinding(
            binding_id=row["binding_id"],
            agent_id=row["agent_id"],
            natal_profile_id=row["natal_profile_id"],
            binding_type=row["binding_type"],
            approved_by=row["approved_by"],
            approved_at=row["approved_at"],
            status=BindingStatus(row["status"]),
            audit_stream_id=row["audit_stream_id"],
        )

    def get_calculation_trace(self, calculation_run_id: str) -> tuple[dict[str, Any], ...]:
        row = self.database.connection.execute(
            "SELECT trace_json FROM bazi_calculation_runs WHERE calculation_run_id=?",
            (calculation_run_id,),
        ).fetchone()
        if row is None:
            raise ValidationError("calculation run does not exist")
        return tuple(json.loads(row[0]))

    def verify_derivation_hash(self, natal_profile_id: str) -> bool:
        return self.verify_derivation_identity(natal_profile_id)

    def _recalculated_profile(self, natal_profile_id: str) -> NatalProfile | None:
        row = self.database.connection.execute(
            """SELECT n.natal_profile_id, n.input_id, n.calculation_run_id,
                      n.rule_profile_id, n.derivation_hash, n.generated_at,
                      r.input_id AS run_input_id,
                      r.rule_profile_id AS run_rule_profile_id,
                      r.algorithm_version, r.ephemeris_version,
                      r.derivation_hash AS run_derivation_hash,
                      r.generated_at AS run_generated_at
               FROM bazi_natal_profiles n
               JOIN bazi_calculation_runs r
                 ON r.calculation_run_id=n.calculation_run_id
               WHERE n.natal_profile_id=?""",
            (natal_profile_id,),
        ).fetchone()
        if row is None:
            return None
        source = self.get_source_input(str(row["input_id"]))
        rules = self.get_rule_profile(str(row["rule_profile_id"]))
        if source is None or rules is None:
            return None
        recalculated = derive_natal_profile(
            source,
            rules,
            calculation_run_id=str(row["calculation_run_id"]),
            natal_profile_id=str(row["natal_profile_id"]),
            generated_at=str(row["generated_at"]),
        )
        identity_matches = (
            row["input_id"] == row["run_input_id"]
            and row["rule_profile_id"] == row["run_rule_profile_id"]
            and row["derivation_hash"] == row["run_derivation_hash"]
            and row["generated_at"] == row["run_generated_at"]
            and row["algorithm_version"] == recalculated.algorithm_version
            and row["ephemeris_version"] == recalculated.ephemeris_version
            and row["derivation_hash"] == recalculated.derivation_hash
        )
        return recalculated if identity_matches else None

    def verify_derivation_identity(self, natal_profile_id: str) -> bool:
        return self._recalculated_profile(natal_profile_id) is not None

    def verify_materialized_facts_integrity(self, natal_profile_id: str) -> bool:
        recalculated = self._recalculated_profile(natal_profile_id)
        if recalculated is None:
            return False
        snapshot = self.database.connection.execute(
            """SELECT materialized_facts_hash, serialization_schema_version,
                      expected_categories_json
               FROM bazi_materialization_snapshots
               WHERE natal_profile_id=?
               ORDER BY materialization_version DESC LIMIT 1""",
            (natal_profile_id,),
        ).fetchone()
        if snapshot is None or snapshot["serialization_schema_version"] != SERIALIZATION_SCHEMA_VERSION:
            return False
        actual_counts = materialized_category_counts(
            self.database.connection, natal_profile_id
        )
        if json.loads(snapshot["expected_categories_json"]) != actual_counts:
            return False
        if materialized_facts_hash(
            self.database.connection, natal_profile_id
        ) != snapshot["materialized_facts_hash"]:
            return False

        pillar_rows = self.database.connection.execute(
            """SELECT pillar_name, stem, branch, fact_json
               FROM bazi_pillars WHERE natal_profile_id=?
               ORDER BY CASE pillar_name
                 WHEN 'YEAR' THEN 0 WHEN 'MONTH' THEN 1
                 WHEN 'DAY' THEN 2 WHEN 'HOUR' THEN 3 ELSE 99 END,
                 pillar_name""",
            (natal_profile_id,),
        ).fetchall()
        expected_pillars = {pillar.name: pillar for pillar in recalculated.pillars}
        if len(pillar_rows) != 4 or set(expected_pillars) != {
            str(row["pillar_name"]) for row in pillar_rows
        }:
            return False
        for row in pillar_rows:
            pillar = expected_pillars[str(row["pillar_name"])]
            if (
                row["stem"] != pillar.stem
                or row["branch"] != pillar.branch
                or row["fact_json"] != canonical_json(pillar)
            ):
                return False

        expected_hidden = [
            (pillar.name, index, hidden)
            for pillar in recalculated.pillars
            for index, hidden in enumerate(pillar.hidden_stems)
        ]
        stored_hidden = [
            (str(row["pillar_name"]), int(row["sequence"]), str(row["hidden_stem"]))
            for row in self.database.connection.execute(
                """SELECT pillar_name, sequence, hidden_stem
                   FROM bazi_hidden_stems WHERE natal_profile_id=?
                   ORDER BY CASE pillar_name
                     WHEN 'YEAR' THEN 0 WHEN 'MONTH' THEN 1
                     WHEN 'DAY' THEN 2 WHEN 'HOUR' THEN 3 ELSE 99 END,
                     pillar_name, sequence""",
                (natal_profile_id,),
            ).fetchall()
        ]
        if stored_hidden != expected_hidden:
            return False

        expected_gods = [
            (pillar.name, index, god)
            for pillar in recalculated.pillars
            for index, god in enumerate(pillar.ten_gods)
        ]
        stored_gods = [
            (str(row["pillar_name"]), int(row["sequence"]), str(row["ten_god"]))
            for row in self.database.connection.execute(
                """SELECT pillar_name, sequence, ten_god
                   FROM bazi_ten_gods WHERE natal_profile_id=?
                   ORDER BY CASE pillar_name
                     WHEN 'YEAR' THEN 0 WHEN 'MONTH' THEN 1
                     WHEN 'DAY' THEN 2 WHEN 'HOUR' THEN 3 ELSE 99 END,
                     pillar_name, sequence""",
                (natal_profile_id,),
            ).fetchall()
        ]
        if stored_gods != expected_gods:
            return False

        relation_rows = self.database.connection.execute(
            """SELECT sequence, relation_type, relation_json
               FROM bazi_relations WHERE natal_profile_id=?
               ORDER BY sequence""",
            (natal_profile_id,),
        ).fetchall()
        expected_relations = [
            (index, str(relation["type"]), canonical_json(relation))
            for index, relation in enumerate(recalculated.relations)
        ]
        stored_relations = [
            (int(row["sequence"]), str(row["relation_type"]), str(row["relation_json"]))
            for row in relation_rows
        ]
        if stored_relations != expected_relations:
            return False

        luck_rows = self.database.connection.execute(
            """SELECT sequence, start_age_years, end_age_years, direction
               FROM bazi_luck_cycles WHERE natal_profile_id=?
               ORDER BY sequence""",
            (natal_profile_id,),
        ).fetchall()
        if luck_rows:
            if [int(row["sequence"]) for row in luck_rows] != list(
                range(1, len(luck_rows) + 1)
            ):
                return False
            if any(
                float(row["start_age_years"]) >= float(row["end_age_years"])
                or str(row["direction"]) not in {item.value for item in LuckDirection}
                for row in luck_rows
            ):
                return False
        return True

    def verify_complete_calculation_integrity(self, natal_profile_id: str) -> bool:
        return (
            self.verify_derivation_identity(natal_profile_id)
            and self.verify_materialized_facts_integrity(natal_profile_id)
        )

    def _required_profile(self, natal_profile_id: str) -> NatalProfile:
        profile = self.get_natal_profile(natal_profile_id)
        if profile is None:
            raise ValidationError("natal profile does not exist")
        return profile

    def runtime_effects(self) -> dict[str, Any]:
        return {
            "bazi_runtime_effect": "NONE",
            "evidence_writeback": False,
            "auto_canonicalization": False,
            "action_authorization": False,
            "privilege_effect": False,
            "stage_promotion": False,
            "subjectivity_claim": False,
            "cloud_calls": 0,
        }
