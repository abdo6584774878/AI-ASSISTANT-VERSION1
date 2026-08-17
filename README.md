# 🤖 AI Assistant

A modular, terminal-based AI assistant built with Python and the Google Gemini API.

The project focuses on clean software architecture, persistent conversations, long-term memory, database management, AI/LLM integration, error handling, and automated testing.

---

## ✨ Features

### 🤖 AI & Gemini Integration
- Google Gemini API integration
- Context-aware conversations
- Automatic conversation title generation
- API error and rate-limit handling
- Configurable assistant backend

### 💾 Conversation System
- Persistent conversations using SQLite
- Multiple conversation support
- Create new conversations
- Switch between conversations
- Rename conversations
- Delete conversations
- Display the current conversation
- Clear conversation history
- Conversation history reconstruction for Gemini

### 🧠 Long-Term Memory
- Automatic memory extraction from user messages
- Persistent memory storage using SQLite
- Memory categories, keys, and values
- Relevant memory search
- Memory context injection into conversations
- Duplicate memory prevention
- Existing memory updates
- Manual memory management through CLI commands

### 🖥️ Terminal Interface
- Command-based interaction
- `/help`
- `/clear`
- `/list`
- `/switch`
- `/new`
- `/current`
- `/rename`
- `/delete`
- `/memory`

### 🧪 Testing
- Comprehensive pytest test suite
- Unit tests for core components
- Command handling tests
- Conversation tests
- Memory tests
- History tests
- Integration tests
- **107 tests currently passing**

---

## 🏗️ Architecture

The project follows a modular architecture that separates the assistant implementation, interface, persistence layer, command handling, and Gemini history management.

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
│   ├── test_assistant.py
│   ├── test_commands.py
│   ├── test_conversation.py
│   ├── test_history.py
│   ├── test_history_integration.py
│   └── test_memory.py
│
├── main.py
├── memory.db
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
└── README.md

🧩 Core Components
assistant/assistant.py
The main AI assistant implementation.
Responsible for:
Gemini API communication
Sending messages
Conversation management
Context construction
Long-term memory retrieval
Automatic memory extraction
Saving and updating memories
Automatic conversation title generation
API error handling
assistant/memory.py
The SQLite persistence layer.
It manages:
Conversations
Messages
Long-term memories
Memory search
Memory creation
Memory retrieval
Memory updates
Memory deletion
Duplicate prevention
assistant/commands.py
Handles terminal commands and user interaction with the assistant's management features.
assistant/history.py
Converts stored conversation messages into the format required by the Gemini API.
assistant/base.py
Defines the common assistant interface.
assistant/fake_assistant.py
Provides a lightweight assistant implementation used for testing without making real Gemini API requests.
assistant/factory.py
Creates the appropriate assistant implementation based on the configured backend.
assistant/config.py
Contains configuration values and backend selection logic.
🧠 Memory System
The assistant has a persistent long-term memory system backed by SQLite.
Memories are stored using:
category
key
value
created_at
updated_at
For example:
[preference] language = Python
[goal] career = Cybersecurity
When the user sends a message, the assistant can:
User message
     ↓
Search relevant memories
     ↓
Build memory context
     ↓
Send context + message to Gemini
     ↓
Generate response
     ↓
Extract potential new memories
     ↓
Save or update memories
This allows the assistant to maintain useful information across conversations and application restarts.
🖥️ Available Commands
Command	Description
/help	Display available commands
/clear	Clear the current conversation history
/list	List all conversations
/switch <id>	Switch to another conversation
/new <title>	Create a new conversation
/current	Display the current conversation
/rename <title>	Rename the current conversation
/delete <id>	Delete a conversation
/exit	Exit the assistant


Memory Commands
Command	Description
/memory add <category> <key> <value>	Create a memory
/memory list	List all stored memories
/memory get <id>	Display a specific memory
/memory update <id> <category> <key> <value>	Update a memory
/memory delete <id>	Delete a memory


Example:
/memory add preference language Python
Then:
/memory list
⚙️ Requirements
Python 3.14+
Google Gemini API key
uv
🚀 Installation
Clone the repository:
git clone https://github.com/abdo6584774878/AI-ASSISTANT-VERSION1.git
cd AI-ASSISTANT-VERSION1
Install the dependencies:
uv sync
Create a .env file in the project root:
GEMINI_API_KEY=your_api_key_here
Start the assistant:
uv run python main.py
Never commit your .env file or expose your API key publicly.

🧪 Testing
The project uses pytest for automated testing.
Run the complete test suite:
uv run pytest
Current status:
107 passed
The test suite covers:
AI assistant behavior
Message sending and persistence
Gemini history reconstruction
Conversation creation
Conversation switching
Conversation renaming
Conversation deletion
Conversation history clearing
Automatic conversation title generation
API error handling
Rate-limit handling
Command handling
Invalid command inputs
SQLite persistence
Memory creation
Memory retrieval
Memory updating
Memory deletion
Memory search
Duplicate memory prevention
Automatic memory extraction
Memory context injection
Memory/history integration
Fake assistant behavior
🛠️ Tech Stack
Python
Google Gemini API
Google GenAI SDK
SQLite
pytest
uv
Git / GitHub
🗺️ Roadmap
The current version establishes the core assistant and persistent memory architecture.
Planned improvements include:
Streaming responses
Tool/function calling
More robust context management
Additional AI backends
Richer terminal interface
Improved configuration system
More advanced memory management
External tools and integrations
Web-based user interface
Deployment as a hosted AI assistant
📚 What I'm Learning
This project is part of my journey toward building more advanced AI systems and strengthening my skills in:
Python
Object-oriented programming
Software architecture
APIs
Databases
SQLite
AI/LLM integration
Prompt engineering
Context management
Long-term memory systems
Error handling
Automated testing
Git and GitHub
🎯 Project Goal
The long-term goal is to evolve this project from a terminal-based AI assistant into a complete AI assistant platform.
The current version focuses on establishing a strong foundation:
Clean Architecture
       +
Persistent Conversations
       +
Long-Term Memory
       +
Reliable Testing
       +
Gemini Integration
       ↓
Future AI Assistant Platform
📄 License
This project is currently intended for educational and portfolio purposes.

After you paste it, **don't change anything else yet**.

Run:

```powershell
pytest -q