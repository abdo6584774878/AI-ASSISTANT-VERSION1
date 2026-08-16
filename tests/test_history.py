from assistant.history import memory_to_gemini_history

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