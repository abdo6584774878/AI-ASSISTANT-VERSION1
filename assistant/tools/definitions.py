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

datetime_declaration = types.FunctionDeclaration(
    name="datetime",
    description="Get the current local date and time.",
    parameters={
        "type": "OBJECT",
        "properties": {},
    },
)

web_search_declaration = types.FunctionDeclaration(
    name="web_search",
    description=(
        "Search the internet for current or up-to-date information. "
        "Use this when the user asks about recent events, current facts, "
        "or information that may have changed."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {
            "query": {
                "type": "STRING",
                "description": "The search query to send to the web search engine.",
            }
        },
        "required": ["query"],
    },
)


calculator_tool = types.Tool(
    function_declarations=[
        calculator_declaration,
        datetime_declaration,
        web_search_declaration,
    ]
)
