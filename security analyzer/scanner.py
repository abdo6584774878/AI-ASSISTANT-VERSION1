import ast
import re

from .models import Finding, SecurityReport
from .rules import get_rule
from .parser import ParsedAgent, ParsedFile


class SecurityScanner:
    """Performs deterministic static security analysis."""

    def scan(self, agent: ParsedAgent) -> SecurityReport:
        findings = []

        for parsed_file in agent.files:
            if parsed_file.language == "python":
                findings.extend(self._scan_python_file(parsed_file))

        score = self._calculate_score(findings)

        return SecurityReport(
            score=score,
            findings=findings,
        )

    def _scan_python_file(self, parsed_file: ParsedFile) -> list[Finding]:
        findings = []

        try:
            tree = ast.parse(parsed_file.content)
        except SyntaxError:
            return findings

        findings.extend(self._check_dynamic_execution(tree, parsed_file))

        findings.extend(self._check_command_execution(tree, parsed_file))

        findings.extend(self._check_hardcoded_secrets(tree, parsed_file))

        findings.extend(self._check_filesystem_access(tree, parsed_file))

        findings.extend(self._check_unsafe_deserialization(tree, parsed_file))

        return findings

    # ---------------------------------------------------------
    # SA-001: eval() / exec()
    # ---------------------------------------------------------

    def _check_dynamic_execution(
        self,
        tree: ast.AST,
        parsed_file: ParsedFile,
    ) -> list[Finding]:
        findings = []
        rule = get_rule("SA-001")

        if rule is None:
            return findings

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            if isinstance(node.func, ast.Name) and node.func.id in {
                "eval",
                "exec",
            }:
                findings.append(
                    Finding(
                        title=rule.title,
                        description=rule.description,
                        severity=rule.severity,
                        confidence=0.99,
                        category=rule.category,
                        file=parsed_file.path,
                        line=node.lineno,
                        evidence=self._get_source_line(
                            parsed_file.content,
                            node.lineno,
                        ),
                        recommendation=(
                            "Avoid eval() and exec(). Use explicit "
                            "parsing or controlled operations instead."
                        ),
                    )
                )

        return findings

    # ---------------------------------------------------------
    # SA-002: subprocess / os.system / shell execution
    # ---------------------------------------------------------

    def _check_command_execution(
        self,
        tree: ast.AST,
        parsed_file: ParsedFile,
    ) -> list[Finding]:
        findings = []
        rule = get_rule("SA-002")

        if rule is None:
            return findings

        dangerous_functions = {
            "os.system",
            "os.popen",
            "subprocess.run",
            "subprocess.Popen",
            "subprocess.call",
            "subprocess.check_call",
            "subprocess.check_output",
        }

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            call_name = self._get_call_name(node)

            if call_name not in dangerous_functions:
                continue

            confidence = 0.85

            shell_enabled = False

            for keyword in node.keywords:
                if keyword.arg == "shell":
                    if isinstance(keyword.value, ast.Constant):
                        shell_enabled = keyword.value.value is True

            if shell_enabled:
                confidence = 0.98

            findings.append(
                Finding(
                    title=rule.title,
                    description=rule.description,
                    severity=rule.severity,
                    confidence=confidence,
                    category=rule.category,
                    file=parsed_file.path,
                    line=node.lineno,
                    evidence=self._get_source_line(
                        parsed_file.content,
                        node.lineno,
                    ),
                    recommendation=(
                        "Avoid shell=True and never pass untrusted "
                        "input directly to command execution. Prefer "
                        "fixed argument lists and strict validation."
                    ),
                )
            )

        return findings

    # ---------------------------------------------------------
    # SA-003: hardcoded secrets
    # ---------------------------------------------------------

    def _check_hardcoded_secrets(
        self,
        tree: ast.AST,
        parsed_file: ParsedFile,
    ) -> list[Finding]:
        findings = []
        rule = get_rule("SA-003")

        if rule is None:
            return findings

        secret_patterns = [
            r"api[_-]?key",
            r"secret",
            r"password",
            r"passwd",
            r"token",
            r"auth[_-]?token",
            r"access[_-]?key",
            r"private[_-]?key",
        ]

        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue

            if not isinstance(node.value, ast.Constant):
                continue

            if not isinstance(node.value.value, str):
                continue

            value = node.value.value

            if len(value.strip()) < 8:
                continue

            for target in node.targets:
                if not isinstance(target, ast.Name):
                    continue

                variable_name = target.id.lower()

                if any(
                    re.search(pattern, variable_name) for pattern in secret_patterns
                ):
                    findings.append(
                        Finding(
                            title=rule.title,
                            description=rule.description,
                            severity=rule.severity,
                            confidence=0.92,
                            category=rule.category,
                            file=parsed_file.path,
                            line=node.lineno,
                            evidence=self._get_source_line(
                                parsed_file.content,
                                node.lineno,
                            ),
                            recommendation=(
                                "Move secrets into environment variables "
                                "or a dedicated secrets manager."
                            ),
                        )
                    )

                    break

        return findings

    # ---------------------------------------------------------
    # SA-004: filesystem access
    # ---------------------------------------------------------

    def _check_filesystem_access(
        self,
        tree: ast.AST,
        parsed_file: ParsedFile,
    ) -> list[Finding]:
        findings = []
        rule = get_rule("SA-004")

        if rule is None:
            return findings

        dangerous_functions = {
            "open",
            "os.remove",
            "os.unlink",
            "os.rename",
            "os.replace",
            "shutil.copy",
            "shutil.copy2",
            "shutil.move",
            "pathlib.Path.read_text",
            "pathlib.Path.write_text",
            "pathlib.Path.read_bytes",
            "pathlib.Path.write_bytes",
        }

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            call_name = self._get_call_name(node)

            if call_name not in dangerous_functions:
                continue

            confidence = 0.75

            if call_name == "open":
                confidence = 0.82

            findings.append(
                Finding(
                    title=rule.title,
                    description=rule.description,
                    severity=rule.severity,
                    confidence=confidence,
                    category=rule.category,
                    file=parsed_file.path,
                    line=node.lineno,
                    evidence=self._get_source_line(
                        parsed_file.content,
                        node.lineno,
                    ),
                    recommendation=(
                        "Restrict filesystem access to approved paths "
                        "and avoid allowing untrusted input to control "
                        "file paths."
                    ),
                )
            )

        return findings

    # ---------------------------------------------------------
    # SA-005: unsafe deserialization
    # ---------------------------------------------------------

    def _check_unsafe_deserialization(
        self,
        tree: ast.AST,
        parsed_file: ParsedFile,
    ) -> list[Finding]:
        findings = []
        rule = get_rule("SA-005")

        if rule is None:
            return findings

        dangerous_functions = {
            "pickle.load",
            "pickle.loads",
            "yaml.load",
            "yaml.unsafe_load",
            "marshal.load",
            "marshal.loads",
        }

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            call_name = self._get_call_name(node)

            if call_name not in dangerous_functions:
                continue

            findings.append(
                Finding(
                    title=rule.title,
                    description=rule.description,
                    severity=rule.severity,
                    confidence=0.95,
                    category=rule.category,
                    file=parsed_file.path,
                    line=node.lineno,
                    evidence=self._get_source_line(
                        parsed_file.content,
                        node.lineno,
                    ),
                    recommendation=(
                        "Avoid deserializing untrusted data with "
                        "pickle, marshal, or unsafe YAML loaders. "
                        "Use safe formats such as JSON where possible."
                    ),
                )
            )

        return findings

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _get_call_name(self, node: ast.Call) -> str | None:
        if isinstance(node.func, ast.Name):
            return node.func.id

        if isinstance(node.func, ast.Attribute):
            parts = []

            current = node.func

            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value

            if isinstance(current, ast.Name):
                parts.append(current.id)

            return ".".join(reversed(parts))

        return None

    def _get_source_line(
        self,
        content: str,
        line_number: int,
    ) -> str:
        lines = content.splitlines()

        if 1 <= line_number <= len(lines):
            return lines[line_number - 1].strip()

        return ""

    def _calculate_score(self, findings: list[Finding]) -> int:
        score = 100

        penalties = {
            "critical": 30,
            "high": 20,
            "medium": 10,
            "low": 5,
            "info": 0,
        }

        for finding in findings:
            score -= penalties.get(finding.severity, 0)

        return max(0, min(100, score))
