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
def test_delete_command(monkeypatch, capsys):
    assistant = FakeAssistant()

    conversation_id = assistant.memory.create_conversation("Delete Test")

    monkeypatch.setattr("builtins.input", lambda _: "y")

    result = handle_command(
        f"/delete {conversation_id}",
        assistant
    )

    captured = capsys.readouterr()

    assert result == "handled"
    assert f"Conversation {conversation_id} deleted." in captured.out
    assert assistant.memory.get_conversation(conversation_id) is None
def test_delete_command_cancelled(monkeypatch, capsys):
    assistant = FakeAssistant()

    conversation_id = assistant.memory.create_conversation("Keep This")

    monkeypatch.setattr("builtins.input", lambda _: "n")

    result = handle_command(
        f"/delete {conversation_id}",
        assistant
    )

    captured = capsys.readouterr()

    assert result == "handled"
    assert assistant.memory.get_conversation(conversation_id) is not None
    assert "cancelled" in captured.out.lower()
def test_delete_nonexistent_conversation(monkeypatch, capsys):
    assistant = FakeAssistant()

    monkeypatch.setattr("builtins.input", lambda _: "y")

    result = handle_command(
        "/delete 99999",
        assistant
    )

    captured = capsys.readouterr()

    assert result == "handled"
    assert "not found" in captured.out.lower()
def test_delete_without_id(capsys):
    assistant = FakeAssistant()

    result = handle_command("/delete", assistant)

    captured = capsys.readouterr()

    assert result == "handled"
    assert "usage" in captured.out.lower()

def test_unknown_command(capsys):
    assistant = FakeAssistant()

    result = handle_command("/unknown", assistant)

    captured = capsys.readouterr()

    assert result is None
    assert captured.out == ""


def test_switch_prefix_is_not_switch_command(capsys):
    assistant = FakeAssistant()

    result = handle_command("/switches 123", assistant)

    captured = capsys.readouterr()

    assert result is None
    assert captured.out == ""


def test_new_prefix_is_not_new_command(capsys):
    assistant = FakeAssistant()

    result = handle_command("/newthing Test", assistant)

    captured = capsys.readouterr()

    assert result is None
    assert captured.out == ""


def test_rename_prefix_is_not_rename_command(capsys):
    assistant = FakeAssistant()

    result = handle_command("/renameold Title", assistant)

    captured = capsys.readouterr()

    assert result is None
    assert captured.out == ""


def test_delete_prefix_is_not_delete_command(capsys):
    assistant = FakeAssistant()

    result = handle_command("/deleteall 123", assistant)

    captured = capsys.readouterr()

    assert result is None
    assert captured.out == ""
def test_command_is_case_insensitive(capsys):
    assistant = FakeAssistant()

    result = handle_command("  /HELP  ", assistant)

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Available commands:" in captured.out


def test_command_with_extra_spaces(capsys):
    assistant = FakeAssistant()

    result = handle_command("   /switch   9999   ", assistant)

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Conversation with ID 9999 not found." in captured.out


def test_memory_add_command(capsys):
    assistant = FakeAssistant()

    result = handle_command(
        "/memory add preference language Python",
        assistant
    )

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Memory created with ID:" in captured.out

    memories = assistant.memory.get_memories()

    assert len(memories) == 1
    assert memories[0][1] == "preference"
    assert memories[0][2] == "language"
    assert memories[0][3] == "Python"


def test_memory_list_command(capsys):
    assistant = FakeAssistant()

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

    result = handle_command("/memory list", assistant)

    captured = capsys.readouterr()

    assert result == "handled"
    assert "preference" in captured.out
    assert "language" in captured.out
    assert "Python" in captured.out
    assert "goal" in captured.out
    assert "career" in captured.out
    assert "Cybersecurity" in captured.out


def test_memory_get_command(capsys):
    assistant = FakeAssistant()

    memory_id = assistant.memory.create_memory(
        "project",
        "current",
        "AI Assistant"
    )

    result = handle_command(
        f"/memory get {memory_id}",
        assistant
    )

    captured = capsys.readouterr()

    assert result == "handled"
    assert "AI Assistant" in captured.out
    assert "project" in captured.out


def test_memory_delete_command(capsys):
    assistant = FakeAssistant()

    memory_id = assistant.memory.create_memory(
        "preference",
        "language",
        "Python"
    )

    result = handle_command(
        f"/memory delete {memory_id}",
        assistant
    )

    captured = capsys.readouterr()

    assert result == "handled"
    assert f"Memory {memory_id} deleted." in captured.out
    assert assistant.memory.get_memory(memory_id) is None


def test_memory_without_subcommand(capsys):
    assistant = FakeAssistant()

    result = handle_command("/memory", assistant)

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Usage:" in captured.out

def test_memory_add_without_arguments(capsys):
    assistant = FakeAssistant()

    result = handle_command(
        "/memory add",
        assistant
    )

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Usage: /memory add <category> <key> <value>" in captured.out


def test_memory_add_missing_value(capsys):
    assistant = FakeAssistant()

    result = handle_command(
        "/memory add preference language",
        assistant
    )

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Usage: /memory add <category> <key> <value>" in captured.out


def test_memory_get_without_id(capsys):
    assistant = FakeAssistant()

    result = handle_command(
        "/memory get",
        assistant
    )

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Usage: /memory get <memory_id>" in captured.out


def test_memory_get_invalid_id(capsys):
    assistant = FakeAssistant()

    result = handle_command(
        "/memory get abc",
        assistant
    )

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Invalid memory ID" in captured.out


def test_memory_get_nonexistent_id(capsys):
    assistant = FakeAssistant()

    result = handle_command(
        "/memory get 9999",
        assistant
    )

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Memory 9999 not found." in captured.out


def test_memory_delete_without_id(capsys):
    assistant = FakeAssistant()

    result = handle_command(
        "/memory delete",
        assistant
    )

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Usage: /memory delete <memory_id>" in captured.out


def test_memory_delete_invalid_id(capsys):
    assistant = FakeAssistant()

    result = handle_command(
        "/memory delete abc",
        assistant
    )

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Invalid memory ID" in captured.out


def test_memory_delete_nonexistent_id(capsys):
    assistant = FakeAssistant()

    result = handle_command(
        "/memory delete 9999",
        assistant
    )

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Memory 9999 not found." in captured.out


def test_unknown_memory_subcommand(capsys):
    assistant = FakeAssistant()

    result = handle_command(
        "/memory something",
        assistant
    )

    captured = capsys.readouterr()

    assert result == "handled"
    assert "Usage: /memory <add|list|get|delete>" in captured.out