import ast


class TaintAnalyzer:
    """Provides shared taint-analysis utilities for security rules."""

    INPUT_SOURCES = {
        "input",
        "request.args.get",
        "request.form.get",
        "request.json.get",
        "request.get_json",
    }

    def get_call_name(self, node: ast.Call) -> str | None:
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

    def find_input_variables(self, tree: ast.AST) -> set[str]:
        """Find variables directly receiving untrusted input."""
        tainted_variables: set[str] = set()

        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue

            if not isinstance(node.value, ast.Call):
                continue

            call_name = self.get_call_name(node.value)

            if call_name not in self.INPUT_SOURCES:
                continue

            for target in node.targets:
                if isinstance(target, ast.Name):
                    tainted_variables.add(target.id)

        return tainted_variables

    def propagate_assignments(
        self,
        tree: ast.AST,
        tainted_variables: set[str],
    ) -> set[str]:
        """Propagate taint through simple variable assignments."""
        changed = True

        while changed:
            changed = False

            for node in ast.walk(tree):
                if not isinstance(node, ast.Assign):
                    continue

                if not isinstance(node.value, ast.Name):
                    continue

                if node.value.id not in tainted_variables:
                    continue

                for target in node.targets:
                    if not isinstance(target, ast.Name):
                        continue

                    if target.id not in tainted_variables:
                        tainted_variables.add(target.id)
                        changed = True

        return tainted_variables
