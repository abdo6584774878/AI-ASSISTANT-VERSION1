from assistant.memory import Memory
from assistant.history import memory_to_gemini_history


memory = Memory()

conversation_id = memory.create_conversation("History Test")

memory.add_message(
    conversation_id,
    "user",
    "Hello"
)

memory.add_message(
    conversation_id,
    "assistant",
    "Hi! How can I help?"
)

messages = memory.get_messages(conversation_id)

print("Messages from SQLite:")
print(messages)

history = memory_to_gemini_history(messages)

print("\nConverted Gemini history:")

for item in history:
    print(item)
    
def test_history_integration():
    memory = Memory(":memory:")

    conversation_id = memory.create_conversation("Integration Test")

    memory.add_message(
        conversation_id,
        "user",
        "Hello"
    )

    memory.add_message(
        conversation_id,
        "assistant",
        "Hi!"
    )

    messages = memory.get_messages(conversation_id)
    history = memory_to_gemini_history(messages)

    assert len(history) == 2
    assert history[0].role == "user"
    assert history[0].parts[0].text == "Hello"
    assert history[1].role == "model"
    assert history[1].parts[0].text == "Hi!"