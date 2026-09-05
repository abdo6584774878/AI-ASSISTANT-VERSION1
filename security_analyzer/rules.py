from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityRule:
    rule_id: str
    title: str
    description: str
    severity: str
    category: str


RULES = {
    "SA-001": SecurityRule(
        rule_id="SA-001",
        title="Dangerous Dynamic Code Execution",
        description=(
            "The agent uses eval() or exec(), which can execute "
            "untrusted code dynamically."
        ),
        severity="critical",
        category="code-execution",
    ),
    "SA-002": SecurityRule(
        rule_id="SA-002",
        title="Dangerous Shell Command Execution",
        description=(
            "The agent executes operating-system commands through "
            "shell or subprocess functionality."
        ),
        severity="high",
        category="command-execution",
    ),
    "SA-003": SecurityRule(
        rule_id="SA-003",
        title="Potential Hardcoded Secret",
        description=(
            "A possible API key, password, token, or other secret "
            "appears directly in the source code."
        ),
        severity="critical",
        category="secrets",
    ),
    "SA-004": SecurityRule(
        rule_id="SA-004",
        title="Arbitrary Filesystem Access",
        description=(
            "The agent may read, write, delete, or manipulate files "
            "without sufficient restrictions."
        ),
        severity="high",
        category="filesystem",
    ),
    "SA-005": SecurityRule(
        rule_id="SA-005",
        title="Unsafe Deserialization",
        description=(
            "The agent uses deserialization mechanisms that can execute "
            "malicious code when processing untrusted data."
        ),
        severity="critical",
        category="deserialization",
    ),
    "SA-006": SecurityRule(
        rule_id="SA-006",
        title="Potential SQL Injection",
        description=(
            "The agent constructs SQL queries using potentially "
            "untrusted or dynamically constructed input."
        ),
        severity="high",
        category="sql-injection",
    ),
    "SA-007": SecurityRule(
        rule_id="SA-007",
        title="Potential Path Traversal",
        description=(
            "The agent constructs filesystem paths using potentially "
            "untrusted input, which may allow access to files outside "
            "the intended directory."
        ),
        severity="high",
        category="path-traversal",
    ),
}


def get_rule(rule_id: str) -> SecurityRule | None:
    return RULES.get(rule_id)


def get_all_rules() -> list[SecurityRule]:
    return list(RULES.values())
