


def handle_command(command, assistant):
    parts = command.strip().split(maxsplit=1)
    command_name = parts[0].lower() if parts else ""

    if command_name == "/exit":
        return "exit"
    
    
    if command_name == "/help":
        print("Available commands:")
        print("- /help: Show available commands")
        print("- /clear: Clear chat history")
        print("- /exit: Exit the chat")
        print("- /list: List all conversations")
        print("- /switch <conversation_id>: Switch to a specific conversation")
        print("- /new <conversation_title>: Create a new conversation")
        print("- /current: Show the current conversation")
        print("- /rename <new_title>: Rename the current conversation")
        print("- /delete <conversation_id>: Delete a specific conversation")
        print("/memory add <category> <key> <value>: Add a memory")
        print("/memory list: List all memories")
        print("- /memory get <memory_id>: Show a specific memory")
        print("- /memory update <id> <category> <key> <value>: Update a memory")
        print("- /memory delete <memory_id>: Delete a memory")
        return "handled"
    
    if command_name == "/clear":
        assistant.clear_chat_history()
        print("Chat history cleared.")
        return "handled"
    
    
    if command_name == "/list":
        conversations = assistant.list_conversations()
        if not conversations:
            print("No conversations found.")
            return "handled"
        print("Conversations:")
        for conversation_id, title, created_at in conversations:
            print(f"{conversation_id}: {title}")
        return "handled"
    
    if command_name == "/switch":
        if len(parts) < 2:
            print("Usage: /switch <conversation_id>")
            return "handled"
        try: 
            conversation_id = int(parts[1])
        except ValueError:
            print("Usage: /switch <conversation_id>")
            return "handled"
        success, _ = assistant.switch_conversation(conversation_id)

        if success:
           print(f"Switched to conversation: {conversation_id}")
        else:
           print(f"Conversation with ID {conversation_id} not found.")
        return "handled"
    
    if command_name == "/new":
        if len(parts) < 2:
            print("Usage: /new <conversation_title>")
            return "handled"
        title = parts[1]
        conversation_id = assistant.create_new_conversation(title)
        print(f"Conversation created with ID: {conversation_id}")
        return "handled"
    
    if command_name == "/current":
        conversation = assistant.get_current_conversation()

        if conversation is None:
            print("No current conversation.")
        else:
            conversation_id, title, created_at = conversation

            print(f"Current Conversation ID: {conversation_id}")
            print(f"Title: {title}")
            print(f"Created At: {created_at}")
        return "handled"
   
    if command_name == "/rename":
        if len(parts) < 2:
            print("Usage: /rename <new_title>")
            return "handled"
        title = parts[1].strip()
        assistant.rename_conversation(title)
        print(f"Conversation renamed to: {title}")
        return "handled"
    
    if command_name == "/delete":
        if len(parts) < 2:
            print("Usage: /delete <conversation_id>")
            return "handled"
        try:
            conversation_id = int(parts[1])
        except ValueError:
            print("Invalid conversation ID. It should be an integer.")
            return "handled"
        
        if conversation_id == assistant.get_current_conversation_id():
            print("Cannot delete the current conversation. Please switch to another conversation first.")
            return "handled"
        conversation = assistant.get_conversation(conversation_id)
        if conversation is None:
            print(f"conversation {conversation_id} not found")
            return "handled"
        print(f"Conversation: {conversation[1]}")
        confirmation  = input("Are you sure you want to delete it? (y/n) : ")
        if confirmation.lower() != "y":
            print("deletion cancelled")
            return "handled"
        success = assistant.delete_conversation(conversation_id)
        if success:
            print(f"Conversation {conversation_id} deleted.")
        else:
            print(f"Conversation {conversation_id} could not be deleted.")
            
        return "handled"
    if command_name == "/memory":
        if len(parts) < 2:
            print("Usage: /memory <add|list|get|delete> ...")
            return "handled"

        memory_parts = parts[1].split(maxsplit=1)
        subcommand = memory_parts[0].lower()

        if subcommand == "add":
            if len(memory_parts) < 2:
                print("Usage: /memory add <category> <key> <value>")
                return "handled"

            args = memory_parts[1].split(maxsplit=2)

            if len(args) < 3:
                print("Usage: /memory add <category> <key> <value>")
                return "handled"

            category, key, value = args

            memory_id = assistant.memory.create_memory(
                category,
                key,
                value
            )

            print(f"Memory created with ID: {memory_id}")
            return "handled"

        if subcommand == "list":
            memories = assistant.memory.get_memories()

            if not memories:
                print("No memories found.")
                return "handled"

            print("Memories:")

            for memory_id, category, key, value, created_at, updated_at in memories:
                print(
                    f"{memory_id}: "
                    f"[{category}] {key} = {value}"
                )

            return "handled"

        if subcommand == "get":
            if len(memory_parts) < 2:
                print("Usage: /memory get <memory_id>")
                return "handled"

            try:
                memory_id = int(memory_parts[1])
            except ValueError:
                print("Invalid memory ID. It should be an integer.")
                return "handled"

            memory = assistant.memory.get_memory(memory_id)

            if memory is None:
                print(f"Memory {memory_id} not found.")
                return "handled"

            _, category, key, value, created_at, updated_at = memory

            print(f"ID: {memory_id}")
            print(f"Category: {category}")
            print(f"Key: {key}")
            print(f"Value: {value}")
            print(f"Created At: {created_at}")
            print(f"Updated At: {updated_at}")

            return "handled"

        if subcommand == "delete":
            if len(memory_parts) < 2:
                print("Usage: /memory delete <memory_id>")
                return "handled"

            try:
                memory_id = int(memory_parts[1])
            except ValueError:
                print("Invalid memory ID. It should be an integer.")
                return "handled"

            success = assistant.memory.delete_memory(memory_id)

            if success:
                print(f"Memory {memory_id} deleted.")
            else:
                print(f"Memory {memory_id} not found.")
            return "handled"
            
        if subcommand == "update":
            if len(memory_parts) < 2:
                print("Usage: /memory update <id> <category> <key> <value>")
                return "handled"
                
            args = memory_parts[1].split(maxsplit=3)
                
            if len(args) < 4:
                print("Usage: /memory update <id> <category> <key> <value>")
                return "handled"
                
            try:
                memory_id = int(args[0])
            except ValueError:
                print("Invalid memory ID. It should be an integer.")
                return "handled"
                
            category, key, value = args[1:]
                
            success = assistant.memory.update_memory(
                memory_id,
                category,
                key,
                value
            )
            if success:
                print(f"Memory {memory_id} updated.")
            else:
                print(f"Memory {memory_id} not found.")
            return "handled"
                
           

        print("Usage: /memory <add|list|get|update|delete>")
        return "handled"
    return None
