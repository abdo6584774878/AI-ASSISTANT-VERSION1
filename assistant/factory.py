from assistant.assistant import AIAssistant
from assistant.fake_assistant import FakeAssistant



def create_assistant(backend, user_id=None):
    if backend == "gemini":
        if user_id is None:
            raise ValueError("user_id is required for Gemini assistant.")

        return AIAssistant(user_id)

    if backend == "fake":
        return FakeAssistant()

    raise ValueError(
        f"Unknown backend: {backend}. "
        "Please set ASSISTANT_BACKEND to 'gemini' or 'fake'."
    )