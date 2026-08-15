from assistant.memory import Memory
from assistant.history import memory_to_gemini_history


memory = Memory()

messages = memory.get_messages()

print("Messages from SQLite:")
print(messages)

history = memory_to_gemini_history(messages)

print("\nConverted Gemini history:")

for item in history:
    print(item)