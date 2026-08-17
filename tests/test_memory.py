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
def test_memory_persists_between_instances(tmp_path):
    db_path = tmp_path / "memory.db"

    memory1 = Memory(str(db_path))

    conversation_id = memory1.create_conversation(
        "Persistent Conversation"
    )

    memory1.add_message(
        conversation_id,
        "user",
        "This should survive."
    )

    del memory1

    memory2 = Memory(str(db_path))

    conversation = memory2.get_conversation(conversation_id)
    messages = memory2.get_messages(conversation_id)

    assert conversation is not None
    assert conversation[1] == "Persistent Conversation"
    assert messages == [
        ("user", "This should survive.")
    ]

def test_create_memory():
    memory = Memory(":memory:")

    memory_id = memory.create_memory(
        "preference",
        "language",
        "Python"
    )

    result = memory.get_memory(memory_id)

    assert result is not None
    assert result[0] == memory_id
    assert result[1] == "preference"
    assert result[2] == "language"
    assert result[3] == "Python"
    assert result[4] is not None
    assert result[5] is not None


def test_get_memories():
    memory = Memory(":memory:")

    memory.create_memory(
        "preference",
        "language",
        "Python"
    )

    memory.create_memory(
        "goal",
        "career",
        "Cybersecurity"
    )

    memories = memory.get_memories()

    assert len(memories) == 2


def test_update_memory():
    memory = Memory(":memory:")

    memory_id = memory.create_memory(
        "preference",
        "language",
        "Python"
    )

    success = memory.update_memory(
        memory_id,
        "preference",
        "language",
        "Rust"
    )

    assert success is True

    result = memory.get_memory(memory_id)

    assert result[3] == "Rust"


def test_delete_memory():
    memory = Memory(":memory:")

    memory_id = memory.create_memory(
        "preference",
        "language",
        "Python"
    )

    success = memory.delete_memory(memory_id)

    assert success is True
    assert memory.get_memory(memory_id) is None


def test_get_nonexistent_memory():
    memory = Memory(":memory:")

    result = memory.get_memory(9999)

    assert result is None


def test_delete_nonexistent_memory():
    memory = Memory(":memory:")

    result = memory.delete_memory(9999)

    assert result is False


def test_memories_persist_between_instances(tmp_path):
    db_path = tmp_path / "memory.db"

    memory1 = Memory(str(db_path))

    memory_id = memory1.create_memory(
        "project",
        "current",
        "AI Assistant"
    )

    del memory1

    memory2 = Memory(str(db_path))

    result = memory2.get_memory(memory_id)

    assert result is not None
    assert result[1] == "project"
    assert result[2] == "current"
    assert result[3] == "AI Assistant"


def test_search_memories_by_key():
    memory = Memory(":memory:")

    memory.create_memory(
        "preference",
        "language",
        "Python"
    )

    memory.create_memory(
        "goal",
        "career",
        "Cybersecurity"
    )

    results = memory.search_memories("language")

    assert len(results) == 1
    assert results[0][2] == "language"
    assert results[0][3] == "Python"


def test_search_memories_by_value():
    memory = Memory(":memory:")

    memory.create_memory(
        "preference",
        "language",
        "Python"
    )

    results = memory.search_memories("Python")

    assert len(results) == 1
    assert results[0][2] == "language"
    assert results[0][3] == "Python"


def test_search_memories_case_insensitive():
    memory = Memory(":memory:")

    memory.create_memory(
        "preference",
        "language",
        "Python"
    )

    results = memory.search_memories("python")

    assert len(results) == 1


def test_search_memories_no_results():
    memory = Memory(":memory:")

    memory.create_memory(
        "preference",
        "language",
        "Python"
    )

    results = memory.search_memories("JavaScript")

    assert results == []

