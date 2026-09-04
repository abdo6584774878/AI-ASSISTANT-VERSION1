from collections import defaultdict

from .models import Finding, SecurityReport


class FindingEngine:
    """
    Processes security findings from different analysis sources.

    Responsibilities:
    - Deduplicate findings
    - Normalize severity
    - Normalize confidence
    - Group related findings
    - Calculate the final security score
    """

    SEVERITY_ORDER = {
        "info": 0,
        "low": 1,
        "medium": 2,
        "high": 3,
        "critical": 4,
    }

    SCORE_PENALTIES = {
        "critical": 30,
        "high": 20,
        "medium": 10,
        "low": 5,
        "info": 0,
    }

    def process(
        self,
        findings: list[Finding],
    ) -> SecurityReport:
        normalized = [self._normalize_finding(finding) for finding in findings]

        deduplicated = self._deduplicate(normalized)

        score = self._calculate_score(deduplicated)

        return SecurityReport(
            score=score,
            findings=deduplicated,
        )

    def _normalize_finding(
        self,
        finding: Finding,
    ) -> Finding:
        severity = finding.severity.lower().strip()

        if severity not in self.SEVERITY_ORDER:
            severity = "info"

        confidence = max(
            0.0,
            min(1.0, finding.confidence),
        )

        return Finding(
            title=finding.title.strip(),
            description=finding.description.strip(),
            severity=severity,
            confidence=confidence,
            category=finding.category.strip().lower(),
            file=finding.file,
            line=finding.line,
            evidence=(finding.evidence.strip() if finding.evidence else None),
            recommendation=(
                finding.recommendation.strip() if finding.recommendation else None
            ),
        )

    def _deduplicate(
        self,
        findings: list[Finding],
    ) -> list[Finding]:
        unique_findings = {}

        for finding in findings:
            key = self._finding_key(finding)

            existing = unique_findings.get(key)

            if existing is None:
                unique_findings[key] = finding
                continue

            if finding.confidence > existing.confidence:
                unique_findings[key] = finding

        return list(unique_findings.values())

    def _finding_key(
        self,
        finding: Finding,
    ) -> tuple:
        return (
            finding.category,
            finding.file,
            finding.line,
            finding.title.lower(),
        )

    def _calculate_score(
        self,
        findings: list[Finding],
    ) -> int:
        score = 100

        for finding in findings:
            penalty = self.SCORE_PENALTIES.get(
                finding.severity,
                0,
            )

            score -= penalty

        return max(0, min(100, score))

    def group_by_category(
        self,
        findings: list[Finding],
    ) -> dict[str, list[Finding]]:
        groups = defaultdict(list)

        for finding in findings:
            groups[finding.category].append(finding)

        return dict(groups)

    def group_by_severity(
        self,
        findings: list[Finding],
    ) -> dict[str, list[Finding]]:
        groups = defaultdict(list)

        for finding in findings:
            groups[finding.severity].append(finding)

        return dict(groups)

    def sort_by_severity(
        self,
        findings: list[Finding],
    ) -> list[Finding]:
        return sorted(
            findings,
            key=lambda finding: (
                -self.SEVERITY_ORDER.get(
                    finding.severity,
                    0,
                ),
                -finding.confidence,
            ),
        )
