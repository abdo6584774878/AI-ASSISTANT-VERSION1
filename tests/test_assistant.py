from assistant.assistant import AIAssistant


def test_switch_conversation(monkeypatch):
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    first_id = assistant.memory.create_conversation("First")
    second_id = assistant.memory.create_conversation("Second")

    assistant.conversation_id = first_id

    monkeypatch.setattr(
        assistant,
        "_create_chat",
        lambda: None
    )

    success, message = assistant.switch_conversation(second_id)

    assert success is True
    assert message == "Conversation switched successfully."
    assert assistant.conversation_id == second_id

def test_switch_nonexistent_conversation(monkeypatch):
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    existing_id = assistant.memory.create_conversation("Existing")
    assistant.conversation_id = existing_id

    monkeypatch.setattr(
        assistant,
        "_create_chat",
        lambda: None
    )

    success, message = assistant.switch_conversation(9999)

    assert success is False
    assert message == "Conversation not found."
    assert assistant.conversation_id == existing_id

def test_create_new_conversation(monkeypatch):
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    old_id = assistant.memory.create_conversation("Old")
    assistant.conversation_id = old_id

    monkeypatch.setattr(
        assistant,
        "_create_chat",
        lambda: None
    )

    new_id = assistant.create_new_conversation("Python Learning")

    assert new_id != old_id
    assert assistant.conversation_id == new_id

    conversation = assistant.memory.get_conversation(new_id)

    assert conversation is not None
    assert conversation[1] == "Python Learning"

def test_get_current_conversation(monkeypatch):
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    conversation_id = assistant.memory.create_conversation(
        "Current Conversation"
    )

    assistant.conversation_id = conversation_id

    conversation = assistant.get_current_conversation()

    assert conversation is not None
    assert conversation[0] == conversation_id
    assert conversation[1] == "Current Conversation"
def test_send_message(monkeypatch):
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    conversation_id = assistant.memory.create_conversation("Test")
    assistant.conversation_id = conversation_id

    class FakeResponse:
        text = "Hello! How can I help?"

    class FakeChat:
        def send_message(self, message):
            assert message == "Hello"
            return FakeResponse()

    assistant.chat = FakeChat()

    monkeypatch.setattr(
        assistant,
        "auto_title_conversation",
        lambda message: None
    )

    result = assistant.send_message("Hello")

    assert result == "Hello! How can I help?"

    messages = assistant.memory.get_messages(conversation_id)

    assert messages == [
        ("user", "Hello"),
        ("assistant", "Hello! How can I help?")
    ]

def test_send_message_rate_limit(monkeypatch):
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    conversation_id = assistant.memory.create_conversation("Test")
    assistant.conversation_id = conversation_id

    class FakeChat:
        def send_message(self, message):
            error = Exception("Rate limit")
            error.code = 429
            raise error

    assistant.chat = FakeChat()

    monkeypatch.setattr(
        "assistant.assistant.errors.ClientError",
        Exception
    )

    result = assistant.send_message("Hello")

    assert result == "Rate limit exceeded. Please try again later."
def test_send_message_api_error(monkeypatch):
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    conversation_id = assistant.memory.create_conversation("Test")
    assistant.conversation_id = conversation_id

    class FakeChat:
        def send_message(self, message):
            error = Exception("API error")
            error.code = 500
            raise error

    assistant.chat = FakeChat()

    monkeypatch.setattr(
        "assistant.assistant.errors.ClientError",
        Exception
    )

    result = assistant.send_message("Hello")

    assert result == "An error occurred while processing your message."

def test_auto_title_conversation(monkeypatch):
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    conversation_id = assistant.memory.create_conversation(
        "New Conversation"
    )

    assistant.conversation_id = conversation_id

    monkeypatch.setattr(
        assistant,
        "generate_title",
        lambda message: "Python Lists"
    )

    result = assistant.auto_title_conversation(
        "What is a Python list?"
    )

    assert result == "Python Lists"

    conversation = assistant.memory.get_conversation(
        conversation_id
    )

    assert conversation is not None
    assert conversation[1] == "Python Lists"
def test_generate_title():
    assistant = object.__new__(AIAssistant)

    class FakeResponse:
        text = "  Python Lists  "

    class FakeModels:
        def generate_content(self, **kwargs):
            return FakeResponse()

    class FakeClient:
        models = FakeModels()

    assistant.client = FakeClient()

    result = assistant.generate_title(
        "What is a Python list?"
    )

    assert result == "Python Lists"
def test_generate_title_api_error(monkeypatch):
    assistant = object.__new__(AIAssistant)

    class FakeModels:
        def generate_content(self, **kwargs):
            error = Exception("API error")
            raise error

    class FakeClient:
        models = FakeModels()

    assistant.client = FakeClient()

    monkeypatch.setattr(
        "assistant.assistant.errors.ClientError",
        Exception
    )

    result = assistant.generate_title(
        "What is Python?"
    )

    assert result == "New Conversation"
def test_send_message_auto_titles_new_conversation(monkeypatch):
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    conversation_id = assistant.memory.create_conversation(
        "New Conversation"
    )

    assistant.conversation_id = conversation_id

    class FakeResponse:
        text = "Python is a programming language."

    class FakeChat:
        def send_message(self, message):
            return FakeResponse()

    assistant.chat = FakeChat()

    def fake_auto_title(message):
        assistant.memory.update_conversation_title(
            assistant.conversation_id,
            "Python Programming"
        )
        return "Python Programming"

    monkeypatch.setattr(
        assistant,
        "auto_title_conversation",
        fake_auto_title
    )

    result = assistant.send_message(
        "What is Python?"
    )

    assert result == "Python is a programming language."

    conversation = assistant.memory.get_conversation(
        conversation_id
    )

    assert conversation is not None
    assert conversation[1] == "Python Programming"
def test_send_message_does_not_retitle_named_conversation(monkeypatch):
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    conversation_id = assistant.memory.create_conversation(
        "Python Learning"
    )

    assistant.conversation_id = conversation_id

    class FakeResponse:
        text = "A list stores multiple values."

    class FakeChat:
        def send_message(self, message):
            return FakeResponse()

    assistant.chat = FakeChat()

    def fail_if_called(message):
        raise AssertionError(
            "auto_title_conversation should not be called"
        )

    monkeypatch.setattr(
        assistant,
        "auto_title_conversation",
        fail_if_called
    )

    result = assistant.send_message(
        "What is a Python list?"
    )

    assert result == "A list stores multiple values."

    conversation = assistant.memory.get_conversation(
        conversation_id
    )

    assert conversation is not None
    assert conversation[1] == "Python Learning"

def test_clear_chat_history(monkeypatch):
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    conversation_id = assistant.memory.create_conversation("Test")
    assistant.conversation_id = conversation_id

    assistant.memory.add_message(
        conversation_id,
        "user",
        "Hello"
    )

    assistant.memory.add_message(
        conversation_id,
        "assistant",
        "Hi!"
    )

    chat_recreated = False

    def fake_create_chat():
        nonlocal chat_recreated
        chat_recreated = True

    monkeypatch.setattr(
        assistant,
        "_create_chat",
        fake_create_chat
    )

    assistant.clear_chat_history()

    assert assistant.memory.get_messages(
        conversation_id
    ) == []

    assert assistant.memory.get_conversation(
        conversation_id
    ) is not None

    assert chat_recreated is True
def test_create_chat_uses_saved_history(monkeypatch):
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    conversation_id = assistant.memory.create_conversation("History Test")
    assistant.conversation_id = conversation_id

    assistant.memory.add_message(
        conversation_id,
        "user",
        "Hello"
    )

    assistant.memory.add_message(
        conversation_id,
        "assistant",
        "Hi!"
    )

    captured = {}

    class FakeChats:
        def create(self, **kwargs):
            captured.update(kwargs)
            return "fake-chat"

    class FakeClient:
        chats = FakeChats()

    assistant.client = FakeClient()

    monkeypatch.setattr(
        "assistant.assistant.MODEL_NAME",
        "test-model"
    )

    monkeypatch.setattr(
        "assistant.assistant.SYSTEM_INSTRUCTION",
        "test instruction"
    )

    assistant._create_chat()

    assert assistant.chat == "fake-chat"
    assert captured["model"] == "test-model"
    assert captured["config"].system_instruction == "test instruction"

    history = captured["history"]

    assert len(history) == 2
    assert history[0].role == "user"
    assert history[0].parts[0].text == "Hello"
    assert history[1].role == "model"
    assert history[1].parts[0].text == "Hi!"