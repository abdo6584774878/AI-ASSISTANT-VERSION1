from assistant.memory import Memory

memory = Memory()

memory.add_message("user", "Hello, how are you?")
memory.add_message("assistant", "I'm good, thank you! How can I assist you today?")
memory.add_message("user", "Can you tell me a joke?")

messages = memory.get_messages()

print(messages)

memory.clear_memory()
print(memory.get_messages())