from abc import ABC, abstractmethod

class BaseAssistant(ABC):
    @abstractmethod
    def send_message(self, message):
        pass

    @abstractmethod
    def clear_chat_history(self):
        pass
    
    def get_current_conversation(self):
        return NotImplementedError