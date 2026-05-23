# 🤖 LocalAI Assistant - Persistent Memory Edition

A fully local AI assistant running on your PC with persistent memory, deep learning capabilities, and specialization in FiveM, MTA, and software engineering.

**No cloud APIs. No tracking. Everything stays on your machine.**

## ✨ Key Features

### 🧠 Persistent Memory System
- **Semantic Memory**: Vector embeddings for contextual retrieval
- **Fact Storage**: SQLite database for structured knowledge
- **Conversation History**: Full chat history with session management
- **Automatic Learning**: Extracts and stores facts from every interaction

### 🚀 Local LLM Integration
- Uses **Ollama** for local model serving
- Supports Mistral, Llama2, Neural Chat, and other models
- Step-by-step reasoning with chain-of-thought
- Customizable parameters (temperature, top-p, max tokens)

### 🎯 Specializations
- **FiveM/QBCore/ESX**: Full framework knowledge and patterns
- **MTA: San Andreas**: Complete scripting guide
- **Programming**: Design patterns, best practices, architecture
- **UI/UX Design**: Minimalist design principles and patterns

### 📂 Code Analysis & Learning
- Analyze Lua, Python, JavaScript, C/C++ files
- Extract functions, classes, and patterns
- Learn from entire projects automatically
- Understand project structure and dependencies

### 🛡️ Permission-Based File Operations
- Safe file read/create/edit/delete
- Whitelist-based access control
- Optional confirmation for destructive operations
- Full audit trail

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│      LocalAI Assistant Core             │
├─────────────────────────────────────────┤
│ • LLM Client (Ollama)                   │
│ • Embedding Engine (Sentence Trans.)    │
│ • Reasoning Engine (CoT)                │
├─────────────────────────────────────────┤
│ Memory Layer (RAG)                      │
│ • Vector Store (Chroma)                 │
│ • Fact Store (SQLite)                   │
│ • Conversation History                  │
├─────────────────────────────────────────┤
│ Tools & Specialization                  │
│ • File Tools (with permissions)         │
│ • Code Analyzer                         │
│ • Domain Knowledge Bases                │
└─────────────────────────────────────────┘
```

## 📋 Requirements

**Hardware**:
- Minimum: 16GB RAM, 8GB VRAM
- Recommended: Ryzen 7, RTX 4070, 1TB SSD

**Software**:
- Python 3.10+
- Ollama (for local LLM)
- Dependencies (see requirements.txt)

## 🚀 Installation & Setup

### 1. Install Ollama
Download from https://ollama.ai

```bash
# Pull a model
ollama pull mistral
# or: ollama pull llama2, ollama pull neural-chat

# Start the server
ollama serve
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Assistant

```bash
# Interactive CLI
python cli.py

# Or use Python API
python example_usage.py
```

## 💻 Quick Start

### CLI Usage

```bash
python cli.py

You> /domain fivem
✅ Domain set to: fivem

You> How do I create a job system in QBCore?
🤔 Processing...

🤖 RESPONSE
[Full response with memory context]

You> /learn ./jobs/police.lua
✅ Learned from file

You> /memory
📊 Memory statistics displayed

You> /help
Shows all available commands
```

### Python API

```python
from assistant import LocalAIAssistant

assistant = LocalAIAssistant()

# Chat with memory retrieval
result = assistant.chat(
    "How do I implement ESX jobs?",
    domain="fivem"
)

# Learn from code
assistant.learn_from_file("./script.lua")
assistant.learn_from_project("./my_resource")

# Store preferences
assistant.remember_preference("framework", "QBCore")

# Export memory
assistant.export_memory("./backup")
```

## 🧠 Memory System

The assistant uses a **three-tier memory system**:

1. **Vector Store (Chroma)**: Semantic embeddings for similarity search
2. **Fact Store (SQLite)**: Structured knowledge (triples), preferences, projects
3. **Conversation History**: Full chat sessions with timestamps

Every response updates memory automatically:
- Extracts facts from responses
- Stores Q&A pairs
- Logs interactions for learning
- Updates conversation context

## 🎯 Specializations

Built-in expertise for:
- **FiveM**: QBCore, ESX, RedM frameworks
- **MTA**: San Andreas scripting patterns
- **Programming**: Design patterns, SOLID, clean code
- **Design**: Minimalist UI/UX, accessibility, responsive design

Add custom training data in `brain/training_data/{domain}/`

## 📝 Configuration

Main settings in `config.yaml`:

```yaml
llm:
  provider: "ollama"
  model: "mistral"
  parameters:
    temperature: 0.7
    top_p: 0.9
    max_tokens: 2048

memory:
  retrieval:
    top_k: 5
    similarity_threshold: 0.6
```

## 📂 Directory Structure

```
sss/
├── assistant/              # Main Python package
│   ├── core/              # LLM, embeddings, reasoning
│   ├── memory/            # Vector DB, facts, conversations
│   ├── tools/             # File operations, code analysis
│   ├── specialization/    # Domain knowledge bases
│   └── main.py           # LocalAIAssistant class
├── brain/                # Persistent storage
│   ├── vectors/          # Chroma vector database
│   ├── facts/            # SQLite knowledge base
│   ├── conversations/    # Chat history
│   └── training_data/    # Custom training data
├── workspace/            # User projects for learning
├── logs/                # Execution logs
├── config.yaml          # Configuration file
├── cli.py              # Interactive CLI interface
├── example_usage.py    # Usage examples
└── README.md
```

## 🛡️ Security

- **File Access**: Limited to `./workspace` and `./brain` directories
- **Permissions**: All operations checked against whitelist
- **Confirmation**: Destructive operations require confirmation
- **Local Only**: No external APIs or cloud storage
- **Audit Trail**: All operations logged

## 🔧 Commands Reference

```
/chat <query>           - Chat with specific query
/domain <name>          - Set specialization (fivem, mta, design, programming)
/learn <filepath>       - Learn from a code file
/project <path>         - Analyze and learn from project
/memory                 - Show memory statistics
/pref <key> <value>     - Store user preference
/recall <key>           - Retrieve preference
/export [path]          - Export all memories
/forget                 - Clear all memories (requires confirmation)
/verbose                - Toggle verbose reasoning display
/help                   - Show this help
/exit                   - Exit the program
```

## 📊 What Gets Stored

- All embeddings and semantic vectors
- Facts, preferences, and project metadata
- Complete conversation history
- Interaction logs and feedback
- Code analysis and learned patterns

**Everything is stored locally in the `brain/` directory.**

## ⚙️ Fine-Tuning Performance

### Speed Up:
- Reduce `max_tokens` in config
- Use smaller model (neural-chat vs mistral)
- Increase `similarity_threshold` for fewer retrieved memories
- Disable verbose mode

### Improve Quality:
- Add domain-specific training data
- Increase context window
- Use temperature 0.5-0.7 for consistency
- Train on your specific projects

### Memory Management:
- Monitor vector store size with `/memory`
- Periodically export backups
- Clear old conversations if needed
- Prune low-relevance memories

## 🚀 Extending

### Add a New Specialization
1. Create class in `assistant/specialization/`
2. Define `SYSTEM_PROMPT` and `KNOWLEDGE_BASE`
3. Register in `SpecializationLoader.DOMAINS`

### Add Custom Tools
1. Create in `assistant/tools/`
2. Implement required methods
3. Register in main.py

### Load Training Data
Place files in `brain/training_data/{domain}/`
- `.md`, `.txt`, `.lua`, `.py`, `.js` files are supported
- Automatically discovered and indexed

## 📈 Roadmap

- [ ] Web UI (VS Code-style interface)
- [ ] Voice input/output (OpenAI Whisper compatible)
- [ ] Advanced RAG with document ranking
- [ ] Fine-tuning on custom data
- [ ] Memory summarization and pruning
- [ ] Multi-workspace support
- [ ] Import/export in multiple formats

## 🐛 Troubleshooting

**Ollama connection error**: Make sure `ollama serve` is running
**Out of memory**: Reduce max_tokens or use smaller model
**Slow responses**: Check /memory stats, reduce context size
**Poor answers**: Increase domain-specific training data

## 📜 License

Free to use and modify for personal/organizational use.

## 🎓 Learn More

- `example_usage.py` - Complete API usage examples
- `config.yaml` - Full configuration options
- Each module has docstrings explaining functionality
- Memory system explained in brain/README.md

---

**Your AI assistant. Local. Private. Learning from you.**

Made for developers, scripters, and engineers who value privacy and control.
