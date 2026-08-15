from assistant.history import memory_to_gemini_history

messages = [
    ("user", "Hello, how are you?"),
    ("assistant", "I'm good, thank you! How can I assist you today?"),
    ("user", "Can you tell me a joke?")
]

history = memory_to_gemini_history(messages)

for item in history:
    print(f"Role: {item.role}, Text: {item.parts[0].text}")