from assistant.tools import TOOLS


def execute_tool(name, arguments):
    tool = TOOLS.get(name)

    if tool is None:
        raise ValueError(f"Unknown tool: {name}")

    return tool(**arguments)