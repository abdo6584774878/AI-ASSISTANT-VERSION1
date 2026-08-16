from assistant.commands import handle_command
from assistant.fake_assistant import FakeAssistant


def test_help_command():
    assistant = FakeAssistant()

    result = handle_command("/help", assistant)

    assert result == "handled"
def test_list_command(capsys):
    assistant = FakeAssistant()

    assistant.memory.create_conversation("Python")
    assistant.memory.create_conversation("Cybersecurity")

    result = handle_command("/list", assistant)

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Python" in captured.out
    assert "Cybersecurity" in captured.out
def test_new_command(capsys):
    assistant = FakeAssistant()

    result = handle_command("/new Python Learning", assistant)

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Conversation created with ID:" in captured.out

    conversation = assistant.memory.get_conversation(
        assistant.conversation_id
    )

    assert conversation is not None
    assert conversation[1] == "Python Learning"
def test_current_command(capsys):
    assistant = FakeAssistant()

    conversation_id = assistant.memory.create_conversation("Current Test")
    assistant.conversation_id = conversation_id

    result = handle_command("/current", assistant)

    captured = capsys.readouterr()

    assert result == "handled"
    assert f"Current Conversation ID: {conversation_id}" in captured.out
    assert "Title: Current Test" in captured.out
def test_switch_command(capsys):
    assistant = FakeAssistant()

    first_id = assistant.memory.create_conversation("First")
    second_id = assistant.memory.create_conversation("Second")

    assistant.conversation_id = first_id

    result = handle_command(f"/switch {second_id}", assistant)

    captured = capsys.readouterr()

    assert result == "handled"
    assert f"Switched to conversation: {second_id}" in captured.out
    assert assistant.conversation_id == second_id
def test_clear_command(capsys):
    assistant = FakeAssistant()

    conversation_id = assistant.memory.create_conversation("Clear Test")
    assistant.conversation_id = conversation_id

    assistant.memory.add_message(
        conversation_id,
        "user",
        "Hello"
    )

    result = handle_command("/clear", assistant)

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Chat history cleared." in captured.out
    assert assistant.memory.get_messages(conversation_id) == []
    assert assistant.memory.get_conversation(conversation_id) is not None
def test_rename_command(capsys):
    assistant = FakeAssistant()

    conversation_id = assistant.memory.create_conversation("Old Title")
    assistant.conversation_id = conversation_id

    result = handle_command("/rename New Title", assistant)

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Conversation renamed to: New Title" in captured.out

    conversation = assistant.memory.get_conversation(conversation_id)

    assert conversation is not None
    assert conversation[1] == "New Title"
def test_switch_invalid_id(capsys):
    assistant = FakeAssistant()

    result = handle_command("/switch 9999", assistant)

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Conversation with ID 9999 not found." in captured.out
def test_switch_without_id(capsys):
    assistant = FakeAssistant()

    result = handle_command("/switch", assistant)

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Usage: /switch <conversation_id>" in captured.out
def test_new_without_title(capsys):
    assistant = FakeAssistant()

    result = handle_command("/new", assistant)

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Usage: /new <conversation_title>" in captured.out
def test_exit_command():
    assistant = FakeAssistant()

    result = handle_command("/exit", assistant)

    assert result == "exit"