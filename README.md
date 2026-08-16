
# 🤖 AI Assistant

A modular terminal-based AI assistant built with Python and the Google Gemini API.

The project focuses on clean software architecture, persistent conversation memory, database management, testing, and AI/LLM integration.

## ✨ Features

- 🤖 Google Gemini API integration
- 💾 Persistent conversation memory using SQLite
- 💬 Multiple conversation support
- 🔄 Switch between conversations
- 🆕 Create new conversations
- ✏️ Rename conversations
- 📋 List saved conversations
- 📌 Display the current conversation
- 🧹 Clear conversation history
- 🖥️ Terminal-based command system
- 🧪 Automated test suite with pytest
- 🧩 Modular assistant architecture
- ⚠️ Error and API rate-limit handling
- 🏷️ Automatic conversation title generation

## 🏗️ Architecture

The project is organized into separate components responsible for different parts of the application:

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
│   ├── test_history_integration.py
│   └── test_commands.py
│
├── main.py
├── pyproject.toml
├── uv.lock
├── .python-version
├── .env.example
├── .gitignore
└── README.md
```

### Core Components

**`assistant.py`**

Main AI assistant implementation responsible for Gemini API communication, conversations, message handling, and title generation.

**`memory.py`**

SQLite-based persistence layer responsible for storing conversations and messages.

**`commands.py`**

Handles terminal commands such as creating, switching, renaming, listing, and clearing conversations.

**`history.py`**

Converts stored conversation messages into the format required by the Gemini API.

**`fake_assistant.py`**

Provides a lightweight assistant implementation for testing command behavior without making real API requests.

## ⚙️ Requirements

- Python 3.14+
- Google Gemini API key
- [uv](https://docs.astral.sh/uv/)

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/abdo6584774878/AI-ASSISTANT-VERSION1.git
cd AI-ASSISTANT-VERSION1
```

Install the project dependencies:

```bash
uv sync
```

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Then start the assistant:

```bash
uv run python main.py
```

> Never commit your `.env` file or expose your API key publicly.

## 💻 Available Commands

| Command | Description |
|---|---|
| `/help` | Display available commands |
| `/clear` | Clear the current conversation history |
| `/list` | List all conversations |
| `/switch <id>` | Switch to another conversation |
| `/new <title>` | Create a new conversation |
| `/rename <title>` | Rename the current conversation |
| `/current` | Show the current conversation |
| `/exit` | Exit the assistant |

## 🧠 Memory System

The assistant uses SQLite to persist conversations locally.

Each conversation stores:

- Conversation ID
- Title
- Creation timestamp
- User messages
- Assistant responses

This allows conversations to remain available after restarting the application.

## 🧪 Testing

The project uses `pytest` for automated testing.

Run the complete test suite:

```bash
uv run pytest
```

The test suite covers:

- Conversation creation
- Conversation retrieval
- Conversation renaming
- Conversation switching
- Message storage
- Conversation history
- Gemini history conversion
- Command handling
- Integration between memory and history components
- Invalid command inputs

## 🛠️ Tech Stack

- Python
- Google Gemini API
- Google GenAI SDK
- SQLite
- pytest
- uv

## 🗺️ Roadmap

Planned improvements include:

- Improved conversation title generation
- Better context and memory management
- Streaming responses
- More robust error handling
- Additional AI backends
- Configuration improvements
- Richer terminal interface
- Tool/function calling
- Long-term memory capabilities

## 📚 What I'm Learning

This project is part of my journey toward building more advanced AI systems and strengthening my skills in:

- Python
- Software architecture
- APIs
- Databases
- AI/LLM integration
- Error handling
- Automated testing
- Git and GitHub

## 📄 License

This project is currently intended for educational and portfolio purposes.
```

**One important thing:** don't blindly copy the test filenames in my architecture section. Make sure they match your actual `tests` folder. You can check with:

```powershell
dir tests
```

