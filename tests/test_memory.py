from assistant.memory import Memory


def test_create_conversation():
    memory = Memory(":memory:")

    conversation_id = memory.create_conversation("Test Conversation")

    conversation = memory.get_conversation(conversation_id)

    assert conversation is not None
    assert conversation[0] == conversation_id
    assert conversation[1] == "Test Conversation"
    assert conversation[2] is not None

def test_add_and_get_messages():
    memory = Memory(":memory:")

    conversation_id = memory.create_conversation("Message Test")

    memory.add_message(
        conversation_id,
        "user",
        "Hello"
    )

    memory.add_message(
        conversation_id,
        "assistant",
        "Hi there!"
    )

    messages = memory.get_messages(conversation_id)

    assert len(messages) == 2
    assert messages[0] == ("user", "Hello")
    assert messages[1] == ("assistant", "Hi there!")
    
def test_update_conversation_title():
    memory = Memory(":memory:")

    conversation_id = memory.create_conversation("Old Title")

    memory.update_conversation_title(
        conversation_id,
        "New Title"
    )

    conversation = memory.get_conversation(conversation_id)

    assert conversation[1] == "New Title"
    
def test_delete_conversation():
    memory = Memory(":memory:")

    conversation_id = memory.create_conversation("Delete Test")

    memory.add_message(
        conversation_id,
        "user",
        "This should be deleted"
    )

    success = memory.delete_conversation(conversation_id)

    assert success is True
    assert memory.get_conversation(conversation_id) is None
    assert memory.get_messages(conversation_id) == []
    
def test_clear_memory():
    memory = Memory(":memory:")

    conversation_id = memory.create_conversation("Clear Test")

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

    memory.clear_memory(conversation_id)

    assert memory.get_messages(conversation_id) == []
    assert memory.get_conversation(conversation_id) is not None
    
def test_get_conversations():
    memory = Memory(":memory:")

    first_id = memory.create_conversation("First Conversation")
    second_id = memory.create_conversation("Second Conversation")

    conversations = memory.get_conversations()

    ids = [conversation[0] for conversation in conversations]
    titles = [conversation[1] for conversation in conversations]

    assert first_id in ids
    assert second_id in ids
    assert "First Conversation" in titles
    assert "Second Conversation" in titles

def test_get_latest_conversation():
    memory = Memory(":memory:")

    first_id = memory.create_conversation("First")
    second_id = memory.create_conversation("Latest")

    latest = memory.get_latest_conversation()

    assert latest is not None
    assert latest[0] == second_id
    assert latest[1] == "Latest"


