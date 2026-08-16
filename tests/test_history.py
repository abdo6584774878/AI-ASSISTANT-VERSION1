from assistant.history import memory_to_gemini_history
import pytest

messages = [
    ("user", "Hello, how are you?"),
    ("assistant", "I'm good, thank you! How can I assist you today?"),
    ("user", "Can you tell me a joke?")
]

history = memory_to_gemini_history(messages)

for item in history:
    print(f"Role: {item.role}, Text: {item.parts[0].text}")
    
def test_memory_to_gemini_history():
    messages = [
        ("user", "Hello"),
        ("assistant", "Hi there!"),
    ]

    history = memory_to_gemini_history(messages)

    assert len(history) == 2
    assert history[0].role == "user"
    assert history[0].parts[0].text == "Hello"
    assert history[1].role == "model"
    assert history[1].parts[0].text == "Hi there!"
def test_memory_to_gemini_history_empty():
    history = memory_to_gemini_history([])

    assert history == []
def test_memory_to_gemini_history_preserves_order():
    messages = [
        ("user", "First"),
        ("assistant", "Second"),
        ("user", "Third"),
        ("assistant", "Fourth"),
    ]

    history = memory_to_gemini_history(messages)

    assert [item.role for item in history] == [
        "user",
        "model",
        "user",
        "model",
    ]

    assert [item.parts[0].text for item in history] == [
        "First",
        "Second",
        "Third",
        "Fourth",
    ]



def test_memory_to_gemini_history_invalid_role():
    messages = [
        ("system", "This should be rejected.")
    ]

    with pytest.raises(ValueError, match="Invalid message role"):
        memory_to_gemini_history(messages)

def test_memory_to_gemini_history_empty_message():
    messages = [
        ("user", ""),
        ("assistant", ""),
    ]

    history = memory_to_gemini_history(messages)

    assert len(history) == 2
    assert history[0].parts[0].text == ""
    assert history[1].parts[0].text == ""
def test_memory_to_gemini_history_preserves_unicode():
    messages = [
        ("user", "Hello 👋 مرحبا"),
        ("assistant", "こんにちは"),
    ]

    history = memory_to_gemini_history(messages)

    assert history[0].parts[0].text == "Hello 👋 مرحبا"
    assert history[1].parts[0].text == "こんにちは"