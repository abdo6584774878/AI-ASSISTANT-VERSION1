from security_analyzer.parser import AgentParser
from security_analyzer.scanner import SecurityScanner


def scan_code(tmp_path, code):
    agent_file = tmp_path / "agent.py"
    agent_file.write_text(code)

    agent = AgentParser().parse(str(agent_file))
    return SecurityScanner().scan(agent)


def test_detects_eval(tmp_path):
    report = scan_code(
        tmp_path,
        """
user_input = input("Enter code: ")
result = eval(user_input)
""",
    )

    assert any(
        finding.title == "Dangerous Dynamic Code Execution"
        for finding in report.findings
    )


def test_detects_exec(tmp_path):
    report = scan_code(
        tmp_path,
        """
code = "print('hello')"
exec(code)
""",
    )

    assert any(
        finding.title == "Dangerous Dynamic Code Execution"
        for finding in report.findings
    )


def test_detects_subprocess(tmp_path):
    report = scan_code(
        tmp_path,
        """
import subprocess

subprocess.run(command)
""",
    )

    assert any(
        finding.title == "Dangerous Shell Command Execution"
        for finding in report.findings
    )


def test_detects_shell_true(tmp_path):
    report = scan_code(
        tmp_path,
        """
import subprocess

subprocess.run(command, shell=True)
""",
    )

    finding = next(
        finding
        for finding in report.findings
        if finding.title == "Dangerous Shell Command Execution"
    )

    assert finding.confidence == 0.98


def test_detects_hardcoded_secret(tmp_path):
    report = scan_code(
        tmp_path,
        """
api_key = "super_secret_key_12345"
""",
    )

    assert any(
        finding.title == "Potential Hardcoded Secret" for finding in report.findings
    )


def test_detects_filesystem_access(tmp_path):
    report = scan_code(
        tmp_path,
        """
data = open("secret.txt").read()
""",
    )

    assert any(
        finding.title == "Arbitrary Filesystem Access" for finding in report.findings
    )


def test_detects_unsafe_pickle(tmp_path):
    report = scan_code(
        tmp_path,
        """
import pickle

data = pickle.loads(user_data)
""",
    )

    assert any(finding.title == "Unsafe Deserialization" for finding in report.findings)


def test_detects_unsafe_yaml(tmp_path):
    report = scan_code(
        tmp_path,
        """
import yaml

data = yaml.load(user_data)
""",
    )

    assert any(finding.title == "Unsafe Deserialization" for finding in report.findings)


def test_finding_contains_location(tmp_path):
    report = scan_code(
        tmp_path,
        """
x = 1
result = eval(user_input)
""",
    )

    finding = next(
        finding
        for finding in report.findings
        if finding.title == "Dangerous Dynamic Code Execution"
    )

    assert finding.file is not None
    assert finding.line == 3
    assert finding.evidence == "result = eval(user_input)"


def test_clean_code_has_no_findings(tmp_path):
    report = scan_code(
        tmp_path,
        """
def add(a, b):
    return a + b

result = add(1, 2)
""",
    )

    assert report.findings == []
    assert report.score == 100


def test_detects_sql_injection_concatenation(tmp_path):
    report = scan_code(
        tmp_path,
        """
username = input("Username: ")
query = "SELECT * FROM users WHERE name = '" + username + "'"
cursor.execute(query)
""",
    )

    assert any(
        finding.title == "Potential SQL Injection" for finding in report.findings
    )


def test_detects_sql_injection_f_string(tmp_path):
    report = scan_code(
        tmp_path,
        """
username = input("Username: ")
cursor.execute(
    f"SELECT * FROM users WHERE name = '{username}'"
)
""",
    )

    assert any(
        finding.title == "Potential SQL Injection" for finding in report.findings
    )


def test_detects_sql_injection_percent_formatting(tmp_path):
    report = scan_code(
        tmp_path,
        """
username = input("Username: ")
query = "SELECT * FROM users WHERE name = '%s'" % username
cursor.execute(query)
""",
    )

    assert any(
        finding.title == "Potential SQL Injection" for finding in report.findings
    )


def test_parameterized_sql_is_not_flagged(tmp_path):
    report = scan_code(
        tmp_path,
        """
username = input("Username: ")

cursor.execute(
    "SELECT * FROM users WHERE name = ?",
    (username,)
)
""",
    )

    assert not any(
        finding.title == "Potential SQL Injection" for finding in report.findings
    )


def test_normal_execute_is_not_flagged(tmp_path):
    report = scan_code(
        tmp_path,
        """
query = "SELECT * FROM users"
cursor.execute(query)
""",
    )

    assert not any(
        finding.title == "Potential SQL Injection" for finding in report.findings
    )


def test_sql_injection_finding_metadata(tmp_path):
    report = scan_code(
        tmp_path,
        """
username = input("Username: ")
cursor.execute(
    f"SELECT * FROM users WHERE name = '{username}'"
)
""",
    )

    finding = next(
        finding
        for finding in report.findings
        if finding.title == "Potential SQL Injection"
    )

    assert finding.severity == "high"
    assert finding.category == "sql-injection"
    assert finding.confidence == 0.90
    assert finding.file is not None
    assert finding.line == 3
    assert "cursor.execute(" in finding.evidence


def test_detects_sql_injection_from_input(tmp_path):
    report = scan_code(
        tmp_path,
        """
username = input("Username: ")
query = "SELECT * FROM users WHERE name = '" + username + "'"
cursor.execute(query)
""",
    )

    assert any(
        finding.title == "Potential SQL Injection" for finding in report.findings
    )


def test_constant_dynamic_sql_is_not_flagged(tmp_path):
    report = scan_code(
        tmp_path,
        """
username = "admin"
query = "SELECT * FROM users WHERE name = '" + username + "'"
cursor.execute(query)
""",
    )

    assert not any(
        finding.title == "Potential SQL Injection" for finding in report.findings
    )


def test_propagates_sql_taint_through_assignment(tmp_path):
    code = """
user_input = input("Name: ")
name = user_input
query = "SELECT * FROM users WHERE name = '" + name + "'"
cursor.execute(query)
"""

    report = scan_code(tmp_path, code)

    findings = [
        finding for finding in report.findings if finding.category == "sql-injection"
    ]

    assert len(findings) == 1
    assert findings[0].severity == "high"


def test_propagates_sql_taint_through_function_argument(tmp_path):
    code = """
def find_user(name):
    query = "SELECT * FROM users WHERE name = '" + name + "'"
    cursor.execute(query)

user_input = input("Name: ")
find_user(user_input)
"""

    report = scan_code(tmp_path, code)

    findings = [
        finding for finding in report.findings if finding.category == "sql-injection"
    ]

    assert len(findings) == 1
    assert findings[0].severity == "high"


def test_propagates_sql_taint_through_multiple_function_calls(tmp_path):
    code = """
def execute_search(query):
    cursor.execute(query)

def find_user(name):
    query = "SELECT * FROM users WHERE name = '" + name + "'"
    execute_search(query)

user_input = input("Name: ")
find_user(user_input)
"""

    report = scan_code(tmp_path, code)

    findings = [
        finding for finding in report.findings if finding.category == "sql-injection"
    ]

    assert len(findings) == 1


def test_detects_path_traversal_from_input(tmp_path):
    code = """
filename = input("File: ")
with open("/app/files/" + filename) as f:
    data = f.read()
"""

    report = scan_code(tmp_path, code)

    findings = [
        finding for finding in report.findings if finding.category == "path-traversal"
    ]

    assert len(findings) == 1
    assert findings[0].severity == "high"


def test_detects_tainted_path_directly(tmp_path):
    code = """
filename = input("File: ")
data = open(filename).read()
"""

    report = scan_code(tmp_path, code)

    findings = [
        finding for finding in report.findings if finding.category == "path-traversal"
    ]

    assert len(findings) == 1


def test_constant_path_is_not_flagged(tmp_path):
    code = """
data = open("/app/config.json").read()
"""

    report = scan_code(tmp_path, code)

    findings = [
        finding for finding in report.findings if finding.category == "path-traversal"
    ]

    assert len(findings) == 0


def test_propagates_path_taint_through_assignment(tmp_path):
    code = """
user_input = input("File: ")
filename = user_input
path = "/app/files/" + filename
data = open(path).read()
"""

    report = scan_code(tmp_path, code)

    findings = [
        finding for finding in report.findings if finding.category == "path-traversal"
    ]

    assert len(findings) == 1
