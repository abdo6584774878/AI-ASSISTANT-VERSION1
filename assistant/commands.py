


def handle_command(command, assistant):
    if command.lower() == "/exit":
        return "exit"
    
    
    if command.lower() == "/help":
        print("Available commands:")
        print("- /help: Show available commands")
        print("- /clear: Clear chat history")
        print("- /exit: Exit the chat")
        print("- /list: List all conversations")
        print("- /switch <conversation_id>: Switch to a specific conversation")
        print("- /new <conversation_title>: Create a new conversation")
        print("- /current: Show the current conversation")
        print("- /rename <new_title>: Rename the current conversation")
        return "handled"
    
    if command.lower() == "/clear":
        assistant.clear_chat_history()
        print("Chat history cleared.")
        return "handled"
    
    
    if command.lower() == "/list":
        conversations = assistant.memory.get_conversations()
        if not conversations:
            print("No conversations found.")
            return "handled"
        print("Conversations:")
        for conversation_id, title, created_at in conversations:
            print(f"{conversation_id}: {title}")
        return "handled"
    
    if command.lower().startswith("/switch"):
        try: 
            conversation_id = int(command.split()[1])
        except (IndexError, ValueError):
            print("Usage: /switch <conversation_id>")
            return "handled"
        success = assistant.switch_conversation(conversation_id)
        
        if success:
            print(f"Switched to conversation: {conversation_id}")
        else:
            print(f"Conversation with ID {conversation_id} not found.")
        return "handled"
    
    if command.lower().startswith("/new"):
        parts = command.split(maxsplit=1)
        if len(parts) < 2:
            print("Usage: /new <conversation_title>")
            return "handled"
        title = parts[1]
        conversation_id = assistant.create_new_conversation(title)
        print(f"Conversation created with ID: {conversation_id}")
        return "handled"
    
    if command.lower() == "/current":
        conversation = assistant.get_current_conversation()

        if conversation is None:
            print("No current conversation.")
        else:
            conversation_id, title, created_at = conversation

            print(f"Current Conversation ID: {conversation_id}")
            print(f"Title: {title}")
            print(f"Created At: {created_at}")
        return "handled"
   
    if command.lower().startswith("/rename"):
        parts = command.split(maxsplit=1)
        if len(parts) < 2:
            print("Usage: /rename <new_title>")
            return "handled"
        title = parts[1].strip()
        assistant.memory.update_conversation_title(assistant.conversation_id, title)
        print(f"Conversation renamed to: {title}")
        return "handled"
    return None
