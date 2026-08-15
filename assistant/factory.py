from assistant.assistant import AIAssistant
from assistant.fake_assistant import FakeAssistant

def create_assistant(backend):
    if backend == "gemini":
        return AIAssistant()
    if backend == "fake":
        return FakeAssistant()
    
    raise ValueError(f"Unknown backend: {backend}. Please set ASSISTANT_BACKEND to 'gemini' or 'fake'.")