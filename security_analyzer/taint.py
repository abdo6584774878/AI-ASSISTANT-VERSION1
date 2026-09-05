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

    def propagate_function_arguments(
        self,
        tree: ast.AST,
        tainted_variables: set[str],
    ) -> set[str]:
        """Propagate taint from call arguments into function parameters."""
        function_parameters: dict[str, list[str]] = {}

        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue

            function_parameters[node.name] = [arg.arg for arg in node.args.args]

        changed = True

        while changed:
            changed = False

            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue

                if not isinstance(node.func, ast.Name):
                    continue

                parameters = function_parameters.get(node.func.id)

                if parameters is None:
                    continue

                for index, argument in enumerate(node.args):
                    if index >= len(parameters):
                        break

                    if not isinstance(argument, ast.Name):
                        continue

                    if argument.id not in tainted_variables:
                        continue

                    parameter = parameters[index]

                    if parameter not in tainted_variables:
                        tainted_variables.add(parameter)
                        changed = True

        return tainted_variables

    def propagate_function_dynamic_values(
        self,
        tree: ast.AST,
        dynamic_variables: set[str],
    ) -> set[str]:
        """Propagate dynamically constructed values through function arguments."""
        function_parameters: dict[str, list[str]] = {}

        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue

            function_parameters[node.name] = [arg.arg for arg in node.args.args]

        changed = True

        while changed:
            changed = False

            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue

                if not isinstance(node.func, ast.Name):
                    continue

                parameters = function_parameters.get(node.func.id)

                if parameters is None:
                    continue

                for index, argument in enumerate(node.args):
                    if index >= len(parameters):
                        break

                    if not isinstance(argument, ast.Name):
                        continue

                    if argument.id not in dynamic_variables:
                        continue

                    parameter = parameters[index]

                    if parameter not in dynamic_variables:
                        dynamic_variables.add(parameter)
                        changed = True

        return dynamic_variables

    def find_tainted_return_functions(
        self,
        tree: ast.AST,
        tainted_variables: set[str],
    ) -> set[str]:
       """Find functions whose return values contain tainted data."""
       tainted_functions: set[str] = set()

       for node in ast.walk(tree):
           if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
               continue

           for child in ast.walk(node):
               if not isinstance(child, ast.Return):
                   continue

               if not isinstance(child.value, ast.Name):
                   continue

               if child.value.id in tainted_variables:
                   tainted_functions.add(node.name)

       return tainted_functions

    def propagate_function_returns(
        self,
        tree: ast.AST,
        tainted_functions: set[str],
        tainted_variables: set[str],
    ) -> set[str]:
        """Propagate taint from tainted function returns to caller variables."""
        changed = True

        while changed:
            changed = False

            for node in ast.walk(tree):
                if not isinstance(node, ast.Assign):
                    continue

                if not isinstance(node.value, ast.Call):
                    continue

                if not isinstance(node.value.func, ast.Name):
                    continue

                function_name = node.value.func.id

                if function_name not in tainted_functions:
                    continue

                for target in node.targets:
                    if not isinstance(target, ast.Name):
                        continue

                    if target.id not in tainted_variables:
                        tainted_variables.add(target.id)
                        changed = True

            # Discover newly tainted functions whose return values
            # depend on newly propagated tainted variables.
            new_tainted_functions = self.find_tainted_return_functions(
                tree,
                tainted_variables,
            )

            for function_name in new_tainted_functions:
                if function_name not in tainted_functions:
                    tainted_functions.add(function_name)
                    changed = True

        return tainted_variables
