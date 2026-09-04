from dataclasses import dataclass, field
from pathlib import Path
import ast


@dataclass
class ParsedFile:
    path: str
    language: str
    content: str
    imports: list[str] = field(default_factory=list)
    functions: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    tool_calls: list[str] = field(default_factory=list)


@dataclass
class ParsedAgent:
    root_path: str
    files: list[ParsedFile] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    configs: list[str] = field(default_factory=list)


class AgentParser:
    """Parses an AI agent codebase without making security decisions."""

    SUPPORTED_EXTENSIONS = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".toml": "toml",
    }

    IGNORED_DIRECTORIES = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        ".pytest_cache",
    }

    def parse(self, path: str) -> ParsedAgent:
        root = Path(path)

        if not root.exists():
            raise FileNotFoundError(f"Agent path not found: {path}")

        if root.is_file():
            files = [self._parse_file(root)]
        else:
            files = self._parse_directory(root)

        dependencies = self._find_dependencies(root)

        return ParsedAgent(
            root_path=str(root.resolve()),
            files=files,
            dependencies=dependencies,
        )

    def _parse_directory(self, root: Path) -> list[ParsedFile]:
        parsed_files = []

        for path in root.rglob("*"):
            if not path.is_file():
                continue

            if any(ignored in path.parts for ignored in self.IGNORED_DIRECTORIES):
                continue

            if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            parsed_files.append(self._parse_file(path))

        return parsed_files

    def _parse_file(self, path: Path) -> ParsedFile:
        language = self.SUPPORTED_EXTENSIONS[path.suffix.lower()]

        try:
            content = path.read_text(
                encoding="utf-8",
                errors="replace",
            )
        except OSError as error:
            raise OSError(f"Could not read file {path}: {error}") from error

        parsed_file = ParsedFile(
            path=str(path),
            language=language,
            content=content,
        )

        if language == "python":
            self._parse_python(content, parsed_file)

        return parsed_file

    def _parse_python(
        self,
        content: str,
        parsed_file: ParsedFile,
    ) -> None:
        try:
            tree = ast.parse(content)
        except SyntaxError:
            # The scanner can later report invalid Python syntax.
            return

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):
                for alias in node.names:
                    parsed_file.imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    parsed_file.imports.append(node.module)

            elif isinstance(node, ast.FunctionDef):
                parsed_file.functions.append(node.name)

            elif isinstance(node, ast.AsyncFunctionDef):
                parsed_file.functions.append(node.name)

            elif isinstance(node, ast.ClassDef):
                parsed_file.classes.append(node.name)

            elif isinstance(node, ast.Call):
                tool_name = self._extract_call_name(node)

                if tool_name:
                    parsed_file.tool_calls.append(tool_name)

    def _extract_call_name(self, node: ast.Call) -> str | None:
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

    def _find_dependencies(self, root: Path) -> list[str]:
        dependencies = []

        if root.is_file():
            root = root.parent

        dependency_files = {
            "requirements.txt",
            "pyproject.toml",
            "package.json",
            "package-lock.json",
            "poetry.lock",
        }

        for path in root.rglob("*"):
            if not path.is_file():
                continue

            if path.name not in dependency_files:
                continue

            if any(ignored in path.parts for ignored in self.IGNORED_DIRECTORIES):
                continue

            dependencies.append(str(path))

        return dependencies
