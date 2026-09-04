from security_analyzer.findings import FindingEngine
from security_analyzer.models import Finding


def make_finding(
    severity="high",
    confidence=0.8,
    category="test",
    title="Test finding",
    file="example.py",
    line=10,
):
    return Finding(
        title=title,
        description="Test description",
        severity=severity,
        confidence=confidence,
        category=category,
        file=file,
        line=line,
    )


def test_normalize_severity_and_confidence():
    engine = FindingEngine()

    finding = make_finding(
        severity=" HIGH ",
        confidence=1.5,
        category=" TEST ",
    )

    report = engine.process([finding])

    result = report.findings[0]

    assert result.severity == "high"
    assert result.confidence == 1.0
    assert result.category == "test"


def test_confidence_cannot_go_below_zero():
    engine = FindingEngine()

    finding = make_finding(confidence=-0.5)

    report = engine.process([finding])

    assert report.findings[0].confidence == 0.0


def test_invalid_severity_becomes_info():
    engine = FindingEngine()

    finding = make_finding(severity="unknown")

    report = engine.process([finding])

    assert report.findings[0].severity == "info"


def test_duplicate_findings_are_removed():
    engine = FindingEngine()

    finding1 = make_finding(confidence=0.7)
    finding2 = make_finding(confidence=0.9)

    report = engine.process([finding1, finding2])

    assert report.total_count == 1
    assert report.findings[0].confidence == 0.9


def test_score_calculation():
    engine = FindingEngine()

    findings = [
        make_finding(severity="critical"),
        make_finding(
            severity="high",
            title="Another issue",
            line=20,
        ),
        make_finding(
            severity="medium",
            title="Third issue",
            line=30,
        ),
    ]

    report = engine.process(findings)

    # 100 - 30 - 20 - 10 = 40
    assert report.score == 40


def test_score_never_goes_below_zero():
    engine = FindingEngine()

    findings = [
        make_finding(
            severity="critical",
            title=f"Issue {i}",
            line=i,
        )
        for i in range(10)
    ]

    report = engine.process(findings)

    assert report.score == 0


def test_group_by_category():
    engine = FindingEngine()

    findings = [
        make_finding(category="secrets"),
        make_finding(
            category="filesystem",
            title="Filesystem issue",
        ),
        make_finding(
            category="secrets",
            title="Another secret",
            line=20,
        ),
    ]

    groups = engine.group_by_category(findings)

    assert len(groups["secrets"]) == 2
    assert len(groups["filesystem"]) == 1


def test_group_by_severity():
    engine = FindingEngine()

    findings = [
        make_finding(severity="critical"),
        make_finding(
            severity="high",
            title="High issue",
        ),
        make_finding(
            severity="critical",
            title="Another critical",
            line=20,
        ),
    ]

    groups = engine.group_by_severity(findings)

    assert len(groups["critical"]) == 2
    assert len(groups["high"]) == 1


def test_sort_by_severity():
    engine = FindingEngine()

    findings = [
        make_finding(
            severity="low",
            confidence=0.9,
        ),
        make_finding(
            severity="critical",
            confidence=0.7,
            title="Critical issue",
        ),
        make_finding(
            severity="high",
            confidence=0.8,
            title="High issue",
        ),
    ]

    sorted_findings = engine.sort_by_severity(findings)

    assert sorted_findings[0].severity == "critical"
    assert sorted_findings[1].severity == "high"
    assert sorted_findings[2].severity == "low"


def test_sort_same_severity_by_confidence():
    engine = FindingEngine()

    findings = [
        make_finding(
            severity="high",
            confidence=0.6,
            title="Low confidence",
        ),
        make_finding(
            severity="high",
            confidence=0.95,
            title="High confidence",
            line=20,
        ),
    ]

    sorted_findings = engine.sort_by_severity(findings)

    assert sorted_findings[0].confidence == 0.95
    assert sorted_findings[1].confidence == 0.6
