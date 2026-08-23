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

def test_auto_title_conversation():
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    conversation_id = assistant.memory.create_conversation(
        "New Conversation"
    )

    assistant.conversation_id = conversation_id


    result = assistant.auto_title_conversation(
        "What is a Python list?"
    )

    assert result == "What is a Python list?"

    conversation = assistant.memory.get_conversation(
        conversation_id
    )
    
    assert conversation is not None
    assert conversation[1] == "What is a Python list?"
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


def test_build_memory_context():
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    assistant.memory.create_memory(
        "preference",
        "language",
        "Python"
    )

    assistant.memory.create_memory(
        "goal",
        "career",
        "Cybersecurity"
    )

    context = assistant.build_memory_context(
        "What programming language should I use?"
    )

    assert "Python" in context
    assert "language" in context


def test_build_memory_context_no_memories():
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    context = assistant.build_memory_context(
        "What should I learn?"
    )

    assert context == ""


def test_send_message_uses_memory_context(monkeypatch):
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    conversation_id = assistant.memory.create_conversation("Test")
    assistant.conversation_id = conversation_id

    assistant.memory.create_memory(
        "preference",
        "language",
        "Python"
    )

    class FakeResponse:
        text = "You are learning Python."

    class FakeChat:
        def send_message(self, message):
            assert "Python" in message
            assert "Relevant memories:" in message
            return FakeResponse()

    assistant.chat = FakeChat()

    monkeypatch.setattr(
        assistant,
        "auto_title_conversation",
        lambda message: None
    )

    result = assistant.send_message(
        "What programming language am I learning?"
    )

    assert result == "You are learning Python."


def test_extract_memories(monkeypatch):
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    class FakeResponse:
        text = '[{"category": "preference", "key": "language", "value": "Python"}]'

    class FakeModels:
        def generate_content(self, **kwargs):
            return FakeResponse()

    class FakeClient:
        models = FakeModels()

    assistant.client = FakeClient()

    result = assistant.extract_memories(
        "I prefer Python."
    )

    assert isinstance(result, list)
    assert result == [{
        "category": "preference",
        "key": "language",
        "value": "Python"
    }]

def test_extract_memories_no_memories(monkeypatch):
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    class FakeResponse:
        text = "[]"

    class FakeModels:
        def generate_content(self, **kwargs):
            return FakeResponse()

    class FakeClient:
        models = FakeModels()

    assistant.client = FakeClient()

    result = assistant.extract_memories(
        "What is the weather today?"
    )

    assert result == []


def test_extract_memories_invalid_json():
    assistant = object.__new__(AIAssistant)

    class FakeResponse:
        text = "This is not JSON"

    class FakeModels:
        def generate_content(self, **kwargs):
            return FakeResponse()

    class FakeClient:
        models = FakeModels()

    assistant.client = FakeClient()

    result = assistant.extract_memories(
        "I prefer Python."
    )

    assert result == []


def test_extract_memories_invalid_structure():
    assistant = object.__new__(AIAssistant)

    class FakeResponse:
        text = '{"category": "preference", "key": "language", "value": "Python"}'

    class FakeModels:
        def generate_content(self, **kwargs):
            return FakeResponse()

    class FakeClient:
        models = FakeModels()

    assistant.client = FakeClient()

    result = assistant.extract_memories(
        "I prefer Python."
    )

    assert result == []


def test_extract_memories_skips_invalid_entries():
    assistant = object.__new__(AIAssistant)

    class FakeResponse:
        text = '''
        [
            {
                "category": "preference",
                "key": "language",
                "value": "Python"
            },
            {
                "category": "goal"
            },
            "garbage"
        ]
        '''

    class FakeModels:
        def generate_content(self, **kwargs):
            return FakeResponse()

    class FakeClient:
        models = FakeModels()

    assistant.client = FakeClient()

    result = assistant.extract_memories(
        "I prefer Python."
    )

    assert result == [
        {
            "category": "preference",
            "key": "language",
            "value": "Python"
        }
    ]


def test_save_extracted_memories():
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    memories = [
        {
            "category": "preference",
            "key": "language",
            "value": "Python"
        },
        {
            "category": "goal",
            "key": "career",
            "value": "Cybersecurity"
        }
    ]

    assistant.save_extracted_memories(memories)

    stored = assistant.memory.get_memories()

    assert len(stored) == 2

    assert stored[0][1:] == (
        "preference",
        "language",
        "Python",
        stored[0][4],
        stored[0][5]
    )

    assert stored[1][1:] == (
        "goal",
        "career",
        "Cybersecurity",
        stored[1][4],
        stored[1][5]
    )


def test_send_message_saves_extracted_memories():
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")
    assistant.conversation_id = assistant.memory.create_conversation(
        "Test Conversation"
    )

    class FakeResponse:
        text = "Python is a great choice."

    class FakeChat:
        def send_message(self, message):
            return FakeResponse()

    assistant.chat = FakeChat()

    assistant.build_memory_context = lambda message: ""

    assistant.extract_memories = lambda message: [
        {
            "category": "preference",
            "key": "language",
            "value": "Python"
        }
    ]

    result = assistant.send_message(
        "I prefer Python."
    )

    assert result == "Python is a great choice."

    memories = assistant.memory.get_memories()

    assert len(memories) == 1
    assert memories[0][1:] == (
        "preference",
        "language",
        "Python",
        memories[0][4],
        memories[0][5]
    )


def test_extract_memories_markdown_json():
    assistant = object.__new__(AIAssistant)

    class FakeResponse:
        text = '''```json
[
    {
        "category": "preference",
        "key": "language",
        "value": "Python"
    }
]
```'''

    class FakeModels:
        def generate_content(self, **kwargs):
            return FakeResponse()

    class FakeClient:
        models = FakeModels()

    assistant.client = FakeClient()

    result = assistant.extract_memories(
        "I prefer Python."
    )

    assert result == [
        {
            "category": "preference",
            "key": "language",
            "value": "Python"
        }
    ]


def test_extract_memories_with_extra_text():
    assistant = object.__new__(AIAssistant)

    class FakeResponse:
        text = '''Here are the memories I found:

[
    {
        "category": "preference",
        "key": "language",
        "value": "Python"
    }
]'''

    class FakeModels:
        def generate_content(self, **kwargs):
            return FakeResponse()

    class FakeClient:
        models = FakeModels()

    assistant.client = FakeClient()

    result = assistant.extract_memories(
        "I prefer Python."
    )

    assert result == [
        {
            "category": "preference",
            "key": "language",
            "value": "Python"
        }
    ]


def test_send_message_saves_extracted_memories(monkeypatch):
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")
    assistant.conversation_id = assistant.memory.create_conversation(
        "Test Conversation"
    )

    class FakeResponse:
        text = "You are learning Python."

    class FakeChat:
        def send_message(self, message):
            return FakeResponse()

    assistant.chat = FakeChat()

    monkeypatch.setattr(
        assistant,
        "extract_memories",
        lambda message: [
            {
                "category": "preference",
                "key": "language",
                "value": "Python"
            }
        ]
    )

    result = assistant.send_message(
        "I prefer Python."
    )

    assert result == "You are learning Python."

    memories = assistant.memory.get_memories()

    assert len(memories) == 1
    assert memories[0][1:] == (
        "preference",
        "language",
        "Python",
        memories[0][4],
        memories[0][5]
    )

def test_save_extracted_memories_updates_existing_memory():
    assistant = object.__new__(AIAssistant)

    from assistant.memory import Memory
    assistant.memory = Memory(":memory:")

    assistant.memory.create_memory(
        "preference",
        "language",
        "Python"
    )

    assistant.save_extracted_memories([
        {
            "category": "preference",
            "key": "language",
            "value": "Rust"
        }
    ])

    memories = assistant.memory.get_memories()

    assert len(memories) == 1
    assert memories[0][1] == "preference"
    assert memories[0][2] == "language"
    assert memories[0][3] == "Rust"


def test_handle_tool_call():
    assistant = object.__new__(AIAssistant)

    class FakeFunctionCall:
        name = "calculator"
        args = {
            "expression": "2 + 5"
        }

    assistant._execute_tool_call = lambda name, arguments: 7

    result = assistant._handle_tool_call(
        FakeFunctionCall()
    )

    assert result.function_response.name == "calculator"
    assert result.function_response.response == {
        "result": 7
    }


def test_handle_tool_call_passes_arguments():
    assistant = object.__new__(AIAssistant)

    captured = {}

    def fake_execute(name, arguments):
        captured["name"] = name
        captured["arguments"] = arguments
        return 42

    assistant._execute_tool_call = fake_execute

    class FakeFunctionCall:
        name = "calculator"
        args = {
            "expression": "6 * 7"
        }

    result = assistant._handle_tool_call(
        FakeFunctionCall()
    )

    assert captured["name"] == "calculator"
    assert captured["arguments"] == {
        "expression": "6 * 7"
    }

    assert result.function_response.response == {
        "result": 42
    }

def test_handle_tool_call_handles_error():
    assistant = object.__new__(AIAssistant)

    def fake_execute(name, arguments):
        raise ValueError("Invalid expression")

    assistant._execute_tool_call = fake_execute

    class FakeFunctionCall:
        name = "calculator"
        args = {
            "expression": "invalid"
        }

    result = assistant._handle_tool_call(
        FakeFunctionCall()
    )

    assert result.function_response.name == "calculator"
    assert result.function_response.response == {
        "result": {
            "error": "Invalid expression"
        }
    }

def test_handle_multiple_tool_calls():
    assistant = object.__new__(AIAssistant)

    calls = []

    def fake_execute(name, arguments):
        calls.append((name, arguments))

        if name == "calculator":
            return 10

        return 20

    assistant._execute_tool_call = fake_execute

    class FakeFunctionCall:
        def __init__(self, name, args):
            self.name = name
            self.args = args

    function_calls = [
        FakeFunctionCall(
            "calculator",
            {"expression": "2 + 8"}
        ),
        FakeFunctionCall(
            "calculator",
            {"expression": "10 + 10"}
        ),
    ]

    tool_responses = [
        assistant._handle_tool_call(function_call)
        for function_call in function_calls
    ]

    assert len(tool_responses) == 2

    assert calls == [
        ("calculator", {"expression": "2 + 8"}),
        ("calculator", {"expression": "10 + 10"}),
    ]

    assert tool_responses[0].function_response.response == {
        "result": 10
    }

    assert tool_responses[1].function_response.response == {
        "result": 10
    }

def test_handle_tool_calls():
    assistant = object.__new__(AIAssistant)

    class FakeFunctionCall:
        def __init__(self, name, args):
            self.name = name
            self.args = args

    assistant._execute_tool_call = (
        lambda name, arguments: arguments["value"]
    )

    function_calls = [
        FakeFunctionCall(
            "calculator",
            {"value": 10}
        ),
        FakeFunctionCall(
            "calculator",
            {"value": 20}
        ),
    ]

    results = assistant._handle_tool_calls(
        function_calls
    )

    assert len(results) == 2

    assert results[0].function_response.response == {
        "result": 10
    }

    assert results[1].function_response.response == {
        "result": 20
    }


def test_stream_message_handles_tool_call():
    assistant = object.__new__(AIAssistant)

    class FakeMemory:
        def search_memories(self, message):
            return []

        def add_message(self, *args):
            pass

        def get_conversation(self, conversation_id):
            return None

    assistant.memory = FakeMemory()
    assistant.conversation_id = 1

    class FakeFunctionCall:
        name = "calculator"
        args = {"expression": "2 + 5"}

    class FakePart:
        function_call = FakeFunctionCall()
        text = None

    class FakeContent:
        parts = [FakePart()]

    class FakeCandidate:
        content = FakeContent()

    class FakeResponse:
        candidates = [FakeCandidate()]
        text = None

    class FakeFinalResponse:
        text = "The answer is 7."

    class FakeChat:
        def send_message(self, content):
            if isinstance(content, str):
                return FakeResponse()

            return FakeFinalResponse()

    assistant.chat = FakeChat()
    assistant._handle_tool_calls = lambda calls: ["fake tool response"]

    results = list(assistant.stream_message("2 + 5"))

    assert results == ["The answer is 7."]


def test_stream_message_handles_web_search():
    assistant = object.__new__(AIAssistant)

    class FakeMemory:
        def search_memories(self, message):
            return []

        def add_message(self, *args):
            pass

        def get_conversation(self, conversation_id):
            return None

    assistant.memory = FakeMemory()
    assistant.conversation_id = 1

    class FakeFunctionCall:
        name = "web_search"
        args = {"query": "latest AI news"}

    class FakePart:
        function_call = FakeFunctionCall()
        text = None

    class FakeContent:
        parts = [FakePart()]

    class FakeCandidate:
        content = FakeContent()

    class FakeResponse:
        candidates = [FakeCandidate()]
        text = None

    class FakeFinalResponse:
        text = "Here are the latest AI news results."

    class FakeChat:
        def send_message(self, content):
            if isinstance(content, str):
                return FakeResponse()

            return FakeFinalResponse()

    assistant.chat = FakeChat()

    captured = {}

    def fake_handle_tool_calls(function_calls):
        captured["calls"] = function_calls
        return ["fake web search response"]

    assistant._handle_tool_calls = fake_handle_tool_calls

    results = list(assistant.stream_message("What are the latest AI news?"))

    assert results == ["Here are the latest AI news results."]

    assert len(captured["calls"]) == 1
    assert captured["calls"][0].name == "web_search"
    assert captured["calls"][0].args == {"query": "latest AI news"}
