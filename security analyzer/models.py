from dataclasses import dataclass, field
from typing import Literal

Severity = Literal["critical", "high", "medium", "low", "info"]


@dataclass
class Finding:
    title: str
    description: str
    severity: Severity
    confidence: float
    category: str
    file: str | None = None
    line: int | None = None
    evidence: str | None = None
    recommendation: str | None = None


@dataclass
class SecurityReport:
    score: int
    findings: list[Finding] = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(finding.severity == "critical" for finding in self.findings)

    @property
    def high_count(self) -> int:
        return sum(finding.severity == "high" for finding in self.findings)

    @property
    def medium_count(self) -> int:
        return sum(finding.severity == "medium" for finding in self.findings)

    @property
    def low_count(self) -> int:
        return sum(finding.severity == "low" for finding in self.findings)
