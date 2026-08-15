# 🤖 AI Assistant

A modular terminal-based AI assistant built with Python and the Google Gemini API.

The project is designed with a clean, extensible architecture and currently supports persistent conversation memory, multiple conversations, conversation switching, command handling, and SQLite-based storage.

## ✨ Features

- 🤖 Google Gemini API integration
- 💾 Persistent conversation memory with SQLite
- 💬 Multiple conversation support
- 🔄 Switch between conversations
- 🆕 Create new conversations
- 📋 List saved conversations
- 📌 Display the current conversation
- 🧹 Clear conversation history
- 🛠️ Terminal command system
- 🧪 Automated tests
- 🧩 Modular assistant/backend architecture
- ⚠️ Error handling and API rate-limit handling
- 🔐 Environment-variable based API key management

## 🏗️ Project Structure

```text
AI_ASSISTANT/
│
├── assistant/
│   ├── __init__.py
│   ├── assistant.py
│   ├── base.py
│   ├── commands.py
│   ├── config.py
│   ├── factory.py
│   ├── fake_assistant.py
│   ├── history.py
│   └── memory.py
│
├── tests/
│   ├── test_memory.py
│   ├── test_history.py
│   ├── test_conversations.py
│   └── ...
│
├── main.py
├── pyproject.toml
├── uv.lock
├── .python-version
├── .env.example
├── .gitignore
└── README.md
⚙️ Requirements
Python 3.14+
A Google Gemini API key
uv package manager
🚀 Installation
Clone the repository:
git clone https://github.com/abdo6584774878/AI-ASSISTANT-VERSION1.git
cd AI-ASSISTANT-VERSION1
Create and activate the virtual environment:
uv sync
Create a .env file:
GEMINI_API_KEY=your_api_key_here
Then start the assistant:
uv run python main.py
💻 Available Commands
Command	Description
/help	Display available commands
/clear	Clear the current conversation history
/list	List all conversations
/switch <id>	Switch to another conversation
/new <title>	Create a new conversation
/current	Show the current conversation
/exit	Exit the assistant


🧠 Memory System
The assistant uses SQLite to persist conversations locally.
Each conversation contains:
Conversation ID
Title
Creation timestamp
User messages
Assistant responses
This allows conversations to remain available even after restarting the application.
🧪 Testing
Run the test suite with:
uv run pytest
Individual tests can also be executed directly:
uv run python tests/test_memory.py
🔐 Security
API credentials are loaded through environment variables.
Never commit your .env file or expose your API key.
The repository includes .env.example as a template:
GEMINI_API_KEY=your_api_key_here
🛠️ Tech Stack
Python
Google Gemini API
Google GenAI SDK
SQLite
Pydantic
uv
pytest
🗺️ Roadmap
Planned improvements include:

Improved conversation title generation

Better context and memory management

Streaming responses

More robust error handling

Additional AI backends

Configuration system improvements

Richer terminal interface

Tool/function calling

Long-term memory capabilities
📚 What I'm Learning
This project is part of my journey toward building more advanced AI systems and strengthening my skills in:
Python
Software architecture
APIs
Databases
AI/LLM integration
Error handling
Testing
Git and GitHub
📄 License
This project is currently for educational and portfolio purposes.

