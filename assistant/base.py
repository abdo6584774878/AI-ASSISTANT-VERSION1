# Defines the common interface that every assistant implementation must follow.
# This keeps the rest of the application independent from a specific AI backend.


from abc import ABC, abstractmethod


class BaseAssistant(ABC):

    @abstractmethod
    def send_message(self, message):
        pass

    @abstractmethod
    def clear_chat_history(self):
        pass

    @abstractmethod
    def switch_conversation(self, conversation_id):
        pass

    @abstractmethod
    def create_new_conversation(self, title):
        pass

    @abstractmethod
    def get_current_conversation(self):
        pass

    @abstractmethod
    def get_conversation(self, conversation_id):
        pass

    @abstractmethod
    def list_conversations(self):
        pass

    @abstractmethod
    def rename_conversation(self, title):
        pass

    @abstractmethod
    def delete_conversation(self, conversation_id):
        pass

    @abstractmethod
    def get_current_conversation_id(self):
        pass
