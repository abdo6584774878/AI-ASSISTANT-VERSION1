from assistant.tools.calculator import calculate
from assistant.tools.datetime import get_current_datetime
from assistant.tools.web import web_search

TOOLS = {
    "calculator": calculate,
    "datetime": get_current_datetime,
    "web_search": web_search
}
