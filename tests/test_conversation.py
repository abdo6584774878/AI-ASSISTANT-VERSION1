from assistant.memory import Memory


memory = Memory()

conversation_id = memory.create_conversation(
    "Python Learning"
)

print("Conversation ID:", conversation_id)

memory.add_message(
    conversation_id,
    "user",
    "What is a list?"
)

memory.add_message(
    conversation_id,
    "assistant",
    "A list is a collection of values."
)

messages = memory.get_messages(conversation_id)

print("Messages:")
print(messages)