from aion_research_eval import EqualsExpected, ResearchCase, ResearchDataset, compare_reports, evaluate_dataset

suite = ResearchDataset(
    name="demo",
    cases=(ResearchCase("c1", "hello", "HELLO"), ResearchCase("c2", "world", "WORLD")),
    evaluators=(EqualsExpected(),),
)

good = evaluate_dataset(suite, str.upper, implementation_id="upper")
bad = evaluate_dataset(suite, lambda value: value, implementation_id="identity")
print(compare_reports(good, bad))
