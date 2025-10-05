from src.metta_agent.agent import map_issue


def test_map_issue_missing_alt():
    finding = map_issue("missing_alt")
    assert finding is not None
    assert finding.sc.startswith("1.1.")
    assert finding.severity in {"low", "medium", "high", "critical"}
    assert finding.fix
    assert finding.references
