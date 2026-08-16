
from assistant.memory import Memory


def test_conversation_with_messages():
    memory = Memory(":memory:")

    conversation_id = memory.create_conversation(
        "Python Learning"
    )

    memory.add_message(
        conversation_id,
        "user",
        "What is a list?"
    )

    memory.add_message(
        conversation_id,
        "assistant",
        "A list is a collection of values."
    )

    messages = memory.get_messages(conversation_id)

    assert messages == [
        ("user", "What is a list?"),
        ("assistant", "A list is a collection of values.")
    ]