from assistant.base import BaseAssistant
from assistant.memory import Memory


class FakeAssistant(BaseAssistant):
    def __init__(self):
        self.memory = Memory(":memory:")
        conversation = self.memory.get_latest_conversation()
        if conversation is None:
            self.conversation_id = self.memory.create_conversation(
                "New Conversation"
        )
        else:
            self.conversation_id = conversation[0]


    def send_message(self, message):
        self.memory.add_message(
            self.conversation_id,
            "user",
            message
        )

        response = f"Fake response to: {message}"

        self.memory.add_message(
            self.conversation_id,
            "assistant",
            response
        )

        return response

    def clear_chat_history(self):
        self.memory.clear_memory(
            self.conversation_id
        )

    def switch_conversation(self, conversation_id):
        conversation = self.memory.get_conversation(conversation_id)

        if conversation is None:
          return False, "Conversation not found"

        self.conversation_id = conversation_id
        return True, "Conversation switched successfully"

    def create_new_conversation(self, title):
        self.conversation_id = self.memory.create_conversation(title)
        return self.conversation_id

    def get_current_conversation(self):
        return self.memory.get_conversation(self.conversation_id)

    def list_conversations(self):
        return self.memory.get_conversations()

    def rename_conversation(self, title):
        self.memory.update_conversation_title(
            self.conversation_id,
            title
        )

    def delete_conversation(self, conversation_id):
        return self.memory.delete_conversation(conversation_id)


    def get_conversation(self, conversation_id):
        return self.memory.get_conversation(conversation_id)

    def get_current_conversation_id(self):
        return self.conversation_id
