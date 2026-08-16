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
def test_get_nonexistent_conversation():
    memory = Memory(":memory:")

    conversation = memory.get_conversation(9999)

    assert conversation is None
def test_get_messages_nonexistent_conversation():
    memory = Memory(":memory:")

    messages = memory.get_messages(9999)

    assert messages == []
def test_clear_nonexistent_conversation():
    memory = Memory(":memory:")

    memory.clear_memory(9999)

    assert memory.get_messages(9999) == []
def test_delete_nonexistent_conversation():
    memory = Memory(":memory:")

    result = memory.delete_conversation(9999)

    assert result is False
def test_get_conversation_title():
    memory = Memory(":memory:")

    conversation_id = memory.create_conversation("My Conversation")

    title = memory.get_conversation_title(conversation_id)

    assert title == "My Conversation"
def test_get_conversation_title_nonexistent():
    memory = Memory(":memory:")

    title = memory.get_conversation_title(9999)

    assert title is None
def test_messages_are_isolated_between_conversations():
    memory = Memory(":memory:")

    first_id = memory.create_conversation("First")
    second_id = memory.create_conversation("Second")

    memory.add_message(first_id, "user", "Message for first")
    memory.add_message(second_id, "user", "Message for second")

    first_messages = memory.get_messages(first_id)
    second_messages = memory.get_messages(second_id)

    assert first_messages == [("user", "Message for first")]
    assert second_messages == [("user", "Message for second")]
def test_multiple_messages_preserve_order():
    memory = Memory(":memory:")

    conversation_id = memory.create_conversation("Order Test")

    messages = [
        ("user", "First"),
        ("assistant", "Second"),
        ("user", "Third"),
        ("assistant", "Fourth"),
        ("user", "Fifth"),
    ]

    for role, message in messages:
        memory.add_message(conversation_id, role, message)

    result = memory.get_messages(conversation_id)

    assert result == messages
def test_get_latest_conversation_empty():
    memory = Memory(":memory:")

    latest = memory.get_latest_conversation()

    assert latest is None
def test_update_conversation_title_nonexistent():
    memory = Memory(":memory:")

    memory.update_conversation_title(
        9999,
        "New Title"
    )

    assert memory.get_conversation(9999) is None

