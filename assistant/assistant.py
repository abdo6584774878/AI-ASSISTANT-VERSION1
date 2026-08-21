import logging
import os
import json

from google import genai
from google.genai import errors, types

from assistant.base import BaseAssistant
from assistant.config import MODEL_NAME, SYSTEM_INSTRUCTION

from assistant.memory import Memory
from assistant.history import memory_to_gemini_history

from assistant.tools.executor import execute_tool
from assistant.tools.definitions import calculator_tool

logger = logging.getLogger(__name__)


class AIAssistant(BaseAssistant):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.memory = Memory()
        conversation = self.memory.get_latest_conversation()
        if conversation is None:
            self.conversation_id = self.memory.create_conversation("New Conversation")
        else:
            self.conversation_id = conversation[0]
        self._create_chat()

    def _create_chat(self):
        messages = self.memory.get_messages(self.conversation_id)
        history = memory_to_gemini_history(messages)

        self.chat = self.client.chats.create(
            model=MODEL_NAME,
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                tools=[calculator_tool],
            ),
            history=history,
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
                ),
            )
            return response.text.strip()
        except errors.ClientError as error:
            logger.error("Could not generate conversation title: %s", error)
            return "New Conversation"

    def auto_title_conversation(self, message):
        words = message.strip().split()

        if not words:
            return "New conversation"

        title = " ".join(words[:6])

        if len(words) > 6:
            title += "..."

        self.memory.update_conversation_title(self.conversation_id, title)

        return title

    def build_memory_context(self, message):
        memories = self.memory.search_memories(message)

        if not memories:
            return ""

        lines = ["Relevant memories:"]

        for _, category, key, value, _, _ in memories:
            lines.append(f"- [{category}] {key}: {value}")

        return "\n".join(lines)

    def extract_memories(self, message):
        try:
            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=(
                    "Extract useful long-term memories from the user's message.\n"
                    "Return a JSON array only.\n"
                    "Each memory must contain exactly these fields:\n"
                    "- category\n"
                    "- key\n"
                    "- value\n\n"
                    "Only include information that could be useful in "
                    "future conversations.\n"
                    "If there are no useful memories, return [].\n\n"
                    f"User message: {message}"
                ),
            )
            text = response.text.strip()

            if text.startswith("```"):
                lines = text.splitlines()

                if lines and lines[0].strip().startswith("```"):
                    lines = lines[1:]

                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]

                text = "\n".join(lines).strip()

            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                start = text.find("[")
                end = text.rfind("]")

                if start == -1 or end <= start:
                    return []

                data = json.loads(text[start : end + 1])

            if not isinstance(data, list):
                return []

            memories = []

            for item in data:
                if not isinstance(item, dict):
                    continue

                if not all(field in item for field in ("category", "key", "value")):
                    continue

                memories.append(
                    {
                        "category": str(item["category"]).strip(),
                        "key": str(item["key"]).strip(),
                        "value": str(item["value"]).strip(),
                    }
                )

            return memories

        except (json.JSONDecodeError, TypeError, AttributeError) as error:
            logger.error("Could not parse extracted memories: %s", error)
            return []

        except errors.ClientError as error:
            logger.error("Could not extract memories: %s", error)
            return []

    def save_extracted_memories(self, memories):
        for memory in memories:
            existing_memories = self.memory.search_memories(memory["key"])
            matching_memory = None

            for existing in existing_memories:
                if existing[1] == memory["category"] and existing[2] == memory["key"]:
                    matching_memory = existing
                    break
            if matching_memory:
                self.memory.update_memory(
                    matching_memory[0],
                    memory["category"],
                    memory["key"],
                    memory["value"],
                )
            else:
                self.memory.create_memory(
                    memory["category"], memory["key"], memory["value"]
                )

    def should_extract_memories(self, message):
        memory_triggers = (
            "my ",
            "i am ",
            "i'm ",
            "i like ",
            "i love ",
            "i hate ",
            "i prefer ",
            "my favorite ",
            "i want ",
            "my goal ",
            "i use ",
            "i study ",
            "i work ",
            "i live ",
        )
        message_lower = message.lower().strip()

        return any(message_lower.startswith(trigger) for trigger in memory_triggers)

    def _execute_tool_call(self, name, arguments):
        arguments = arguments or {}

        return execute_tool(name, arguments)

    def send_message(self, message):
        try:
            memory_context = self.build_memory_context(message)

            if memory_context:
                prompt = f"{memory_context}\n\nUser message : {message}"
            else:
                prompt = message

            response = self.chat.send_message(prompt)

            self.memory.add_message(self.conversation_id, "user", message)

            self.memory.add_message(self.conversation_id, "assistant", response.text)

            if self.should_extract_memories(message):
                extracted_memories = self.extract_memories(message)
                self.save_extracted_memories(extracted_memories)

            conversation = self.memory.get_conversation(self.conversation_id)

            if conversation and conversation[1] == "New Conversation":
                self.auto_title_conversation(message)

            return response.text

        except errors.ClientError as error:
            logger.error("An error occurred while processing your message: %s", error)

            if error.code == 429:
                return "Rate limit exceeded. Please try again later."

            return "An error occurred while processing your message."

    def _handle_tool_call(self, function_call):
        try:
            result = self._execute_tool_call(function_call.name, function_call.args)
        except Exception as error:
            logger.error("Tool execution failed: %s", error)

            result = {"error": str(error)}
        return types.Part.from_function_response(
           name=function_call.name,
           response={
               "result" : result
           }
        )

    def _handle_tool_calls(self, function_calls):
        return [
            self._handle_tool_call(function_call)
            for function_call in function_calls
        ]

    def stream_message(self, message):
        try:
            memory_context = self.build_memory_context(message)

            if memory_context:
                prompt = f"{memory_context}\n\nUser message : {message}"
            else:
                prompt = message

            self.memory.add_message(self.conversation_id, "user", message)

            response_parts = []

            for chunk in self.chat.send_message_stream(prompt):
                parts = chunk.candidates[0].content.parts

                function_calls = [
                    part.function_call for part in parts if part.function_call
                ]

                text_parts = [part.text for part in parts if part.text]

                for text in text_parts:
                    response_parts.append(text)
                    yield text

                if function_calls:
                    tool_responses = self._handle_tool_calls(function_calls)

                    for tool_chunk in self.chat.send_message_stream(tool_responses):
                        text = tool_chunk.text or ""

                        if text:
                            response_parts.append(text)
                            yield text

            response_text = "".join(response_parts)

            self.memory.add_message(self.conversation_id, "assistant", response_text)

            if self.should_extract_memories(message):
                extracted_memories = self.extract_memories(message)
                self.save_extracted_memories(extracted_memories)

            conversation = self.memory.get_conversation(self.conversation_id)

            if conversation and conversation[1] == "New Conversation":
                self.auto_title_conversation(message)

        except errors.ClientError as error:
            logger.error("AN ERROR OCCURED WHILE PROCESSING YOUR MESSAGE : %s", error)

            if error.code == 429:
                yield "Rate limit exceeded. Please try again later."
            else:
                yield "An error occured while processing your message."

    def clear_chat_history(self):
        self.memory.clear_memory(self.conversation_id)
        self._create_chat()  # Reinitialize the chat after clearing history

    def list_conversations(self):
        return self.memory.get_conversations()

    def rename_conversation(self, title):
        self.memory.update_conversation_title(self.conversation_id, title)

    def delete_conversation(self, conversation_id):
        return self.memory.delete_conversation(conversation_id)

    def get_conversation(self, conversation_id):
        return self.memory.get_conversation(conversation_id)

    def get_current_conversation_id(self):
        return self.conversation_id
