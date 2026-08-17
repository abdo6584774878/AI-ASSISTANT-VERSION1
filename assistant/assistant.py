
import logging
import os
from google import genai
from google.genai import errors

from assistant.base import BaseAssistant
from assistant.config import MODEL_NAME, SYSTEM_INSTRUCTION

from assistant.memory import Memory
from assistant.history import memory_to_gemini_history

logger = logging.getLogger(__name__)

class AIAssistant(BaseAssistant):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.memory = Memory()
        conversation = self.memory.get_latest_conversation()
        if conversation is None:
            self.conversation_id = self.memory.create_conversation(
                "New Conversation"
            )
        else:
            self.conversation_id = conversation[0]
        self._create_chat()
        
    def _create_chat(self):
        messages = self.memory.get_messages(
            self.conversation_id
        )
        history = memory_to_gemini_history(messages)
        
        self.chat = self.client.chats.create(
            model=MODEL_NAME,
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            ),
            history=history  
        )
    
    def switch_conversation(self, conversation_id):
        conversation = self.memory.get_conversation(conversation_id)
        
        if conversation is None:
            return False, "Conversation not found."
        
        self.conversation_id = conversation_id
        self._create_chat()
        return True, "Conversation switched successfully."
    
    def create_new_conversation(self, title):
        self.conversation_id = self.memory.create_conversation(title)
        self._create_chat()
        return self.conversation_id 
    
    
    def get_current_conversation(self):
        return self.memory.get_conversation(self.conversation_id)
    
    def generate_title(self, message):
        try:
            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=(
                    "Create a very short title for this conversation "
                    "Use 2 to 5 words. Return only the title.\n\n"
                    f"User message: {message}"
                )
            )
            return response.text.strip()
        except errors.ClientError as error:
            logger.error(
                "Could not generate conversation title: %s",
                error
            )
            return "New Conversation"
    def auto_title_conversation(self, message):
        title = self.generate_title(message)
        self.memory.update_conversation_title(
            self.conversation_id,
            title
        )
        return title
    def send_message(self, message):
        try: 
            response = self.chat.send_message(message)
            self.memory.add_message(
                self.conversation_id,
                "user",
                message
            )
            
            self.memory.add_message(
                self.conversation_id,
                "assistant",
                response.text
            )
            conversation = self.memory.get_conversation(self.conversation_id)
            if conversation and conversation[1] == "New Conversation":
                self.auto_title_conversation(message)
            return response.text
           
        except errors.ClientError as error:
            logger.error("An error occurred while processing your message: %s", error)
            if error.code == 429:
                return "Rate limit exceeded. Please try again later."
             
            return "An error occurred while processing your message."
    def clear_chat_history(self):
        self.memory.clear_memory(
            self.conversation_id
        )
        self._create_chat()  # Reinitialize the chat after clearing history
        
    def list_conversations(self):
        return self.memory.get_conversations()
    
    def rename_conversation(self, title):
        self.memory.update_conversation_title(
            self.conversation_id,
            title
        )
    def delete_conversation(self, conversation_id):
        return self.memory.delete_conversation(conversation_id)
    

        
    
    