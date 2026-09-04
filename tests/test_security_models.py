from security_analyzer.models import Finding, SecurityReport


def test_finding_creation():
    finding = Finding(
        title="Test vulnerability",
        description="A test security issue",
        severity="high",
        confidence=0.9,
        category="test",
        file="example.py",
        line=10,
        evidence="dangerous_code()",
        recommendation="Fix the vulnerability",
    )

    assert finding.title == "Test vulnerability"
    assert finding.description == "A test security issue"
    assert finding.severity == "high"
    assert finding.confidence == 0.9
    assert finding.category == "test"
    assert finding.file == "example.py"
    assert finding.line == 10
    assert finding.evidence == "dangerous_code()"
    assert finding.recommendation == "Fix the vulnerability"


def test_security_report_counts():
    findings = [
        Finding(
            title="Critical issue",
            description="Critical",
            severity="critical",
            confidence=1.0,
            category="test",
        ),
        Finding(
            title="High issue",
            description="High",
            severity="high",
            confidence=0.9,
            category="test",
        ),
        Finding(
            title="Medium issue",
            description="Medium",
            severity="medium",
            confidence=0.8,
            category="test",
        ),
        Finding(
            title="Low issue",
            description="Low",
            severity="low",
            confidence=0.7,
            category="test",
        ),
        Finding(
            title="Info",
            description="Info",
            severity="info",
            confidence=0.6,
            category="test",
        ),
    ]

    report = SecurityReport(
        score=50,
        findings=findings,
    )

    assert report.critical_count == 1
    assert report.high_count == 1
    assert report.medium_count == 1
    assert report.low_count == 1
    assert report.info_count == 1
    assert report.total_count == 5


def test_empty_security_report():
    report = SecurityReport(score=100)

    assert report.findings == []
    assert report.critical_count == 0
    assert report.high_count == 0
    assert report.medium_count == 0
    assert report.low_count == 0
    assert report.info_count == 0
    assert report.total_count == 0
