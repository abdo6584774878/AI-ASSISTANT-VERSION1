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