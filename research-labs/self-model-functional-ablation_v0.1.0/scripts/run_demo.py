
from aion_self_model_ablation import default_benchmark_tasks, run_matched_ablation


def main() -> None:
    result = run_matched_ablation(
        default_benchmark_tasks(),
        latent_capability=0.62,
        random_seed=17,
    )
    for summary in result.summaries:
        print(
            summary.condition.value,
            f"reward={summary.total_reward:.2f}",
            f"commit_rate={summary.commit_rate:.2f}",
            f"failure_rate={summary.failure_rate_when_committed:.2f}",
            f"transfer_reward={summary.transfer_reward:.2f}",
        )
    print("interpretation=", result.interpretation)
    print("subjectivity_conclusion=", result.subjectivity_conclusion)


if __name__ == "__main__":
    main()
