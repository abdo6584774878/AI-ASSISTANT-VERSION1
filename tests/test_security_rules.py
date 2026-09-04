from security_analyzer.rules import RULES, get_all_rules, get_rule


def test_all_security_rules_exist():
    expected_rule_ids = {
        "SA-001",
        "SA-002",
        "SA-003",
        "SA-004",
        "SA-005",
        "SA-006",
    }

    assert set(RULES.keys()) == expected_rule_ids


def test_get_all_rules_returns_all_rules():
    rules = get_all_rules()

    assert len(rules) == 6
    assert {rule.rule_id for rule in rules} == {
        "SA-001",
        "SA-002",
        "SA-003",
        "SA-004",
        "SA-005",
        "SA-006",
    }


def test_get_rule():
    rule = get_rule("SA-001")

    assert rule is not None
    assert rule.rule_id == "SA-001"
    assert rule.title == "Dangerous Dynamic Code Execution"
    assert rule.severity == "critical"
    assert rule.category == "code-execution"


def test_get_unknown_rule_returns_none():
    assert get_rule("SA-999") is None


def test_rule_severities():
    assert RULES["SA-001"].severity == "critical"
    assert RULES["SA-002"].severity == "high"
    assert RULES["SA-003"].severity == "critical"
    assert RULES["SA-004"].severity == "high"
    assert RULES["SA-005"].severity == "critical"


def test_rule_categories():
    assert RULES["SA-001"].category == "code-execution"
    assert RULES["SA-002"].category == "command-execution"
    assert RULES["SA-003"].category == "secrets"
    assert RULES["SA-004"].category == "filesystem"
    assert RULES["SA-005"].category == "deserialization"


def test_rules_have_required_metadata():
    for rule in get_all_rules():
        assert rule.rule_id
        assert rule.title
        assert rule.description
        assert rule.severity
        assert rule.category


def test_rules_are_immutable():
    rule = get_rule("SA-001")

    try:
        rule.title = "Modified"
        assert False, "SecurityRule should be immutable"
    except AttributeError:
        pass


def test_sa006_sql_injection_rule():
    rule = get_rule("SA-006")

    assert rule is not None
    assert rule.rule_id == "SA-006"
    assert rule.title == "Potential SQL Injection"
    assert rule.severity == "high"
    assert rule.category == "sql-injection"
