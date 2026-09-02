from scripts.check_local_prerequisites import classify, node_supported
import pytest


@pytest.mark.parametrize("version, expected", [("v20.9.0", False), ("v22.12.0", False),
    ("v22.13.0", True), ("v24.19.0", True), ("garbage", False), ("", False)])
def test_node_version_contract(version, expected):
    assert node_supported(version) is expected


def test_symlink_failure_is_reported_not_labeled_resource_exhaustion():
    problems = classify("python", {"pytest": "9", "jsonschema": "4", "lunar-python": "1"},
                        {"git": True}, {"supported": False, "winerror": 1314})
    assert problems == ["FULL_ROOT_QA_SYMLINK_PREREQUISITE_MISSING"]


def test_missing_tools_and_dependencies_are_separate():
    problems = classify("all", {"lunar-python": None}, {"git": False, "pnpm": False}, {"supported": True})
    assert set(problems) == {"GIT_MISSING", "DEPENDENCY_MISSING:lunar-python", "NODE_22_13_OR_NEWER_REQUIRED", "PNPM_MISSING"}


def test_ziwei_does_not_require_python_test_modules_or_symlinks():
    assert classify("ziwei", {"pytest": None}, {"git": True, "node_version": "v24.19.0", "pnpm": True},
                    {"supported": False}) == []
