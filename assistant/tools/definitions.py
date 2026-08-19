from google.genai import types


calculator_declaration = types.FunctionDeclaration(
    name="calculator",
    description="Calculate a mathematical expression.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "expression": {
                "type": "STRING",
                "description": "The mathematical expression to calculate.",
            }
        },
        "required": ["expression"],
    },
)


calculator_tool = types.Tool(
    function_declarations=[calculator_declaration]
)