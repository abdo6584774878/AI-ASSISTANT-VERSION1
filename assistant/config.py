import os



MODEL_NAME = "gemini-2.5-flash"
SYSTEM_INSTRUCTION = (
    "You are a helpful AI assistant running in a terminal. "
    "give clear and concise answers"
)

def get_assistant_backend():
    return os.getenv("ASSISTANT_BACKEND", "fake")