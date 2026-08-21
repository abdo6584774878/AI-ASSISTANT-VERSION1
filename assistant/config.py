import os


MODEL_NAME = "gemini-2.5-flash"
SYSTEM_INSTRUCTION = (
    "You are a helpful AI assistant running in a terminal. "
    "Give clear and concise answers. "
    "Use the web_search tool when the user asks for current, recent, "
    "or up-to-date information. "
    "When using web_search, base your answer on the returned search results "
    "and do not invent facts that are not supported by them."
)

def get_assistant_backend():
    return os.getenv("ASSISTANT_BACKEND", "fake")
