# 🏗️ LocalAI Assistant - Architecture & Design

Complete technical documentation of the LocalAI Assistant system design, components, and how they work together.

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                        │
│                   (CLI / Python API / Future UI)                │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│              CONVERSATION & QUERY PROCESSING LAYER              │
│  • Parse user intent                                            │
│  • Detect domain (FiveM, MTA, etc.)                             │
│  • Permission checks                                            │
│  • Context building                                             │
└──────────────────────────────┬──────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
    ┌────────────┐      ┌────────────────┐    ┌──────────┐
    │ MEMORY     │      │ LLM REASONING  │    │ TOOLS &  │
    │ RETRIEVAL  │      │ LAYER          │    │ ANALYSIS │
    └────────────┘      └────────────────┘    └──────────┘
        │                      │                      │
        │  RAG Context        │  Chain-of-Thought    │  Code/File
        │  Semantics          │  Step-by-Step        │  Operations
        │  Facts              │  Reasoning           │
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                    SPECIALIZATION LAYER                         │
│  • Domain knowledge bases (FiveM, MTA, Design, Programming)    │
│  • Custom training data injection                              │
│  • System prompts & context formatting                         │
└──────────────────────────────┬──────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
    ┌──────────┐          ┌──────────┐        ┌──────────┐
    │ VECTOR   │          │ FACT     │        │ CONV.    │
    │ STORE    │          │ STORE    │        │ HISTORY  │
    │(Chroma)  │          │(SQLite)  │        │(JSON)    │
    └──────────┘          └──────────┘        └──────────┘
        │                      │                      │
        │ Embeddings          │ Structured            │ Session
        │ Semantic Search     │ Knowledge             │ Management
        │ Similarity Ranking  │ Preferences           │
        │                      │ Projects              │
        │                      │ Interactions          │
        └──────────────────────┼──────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                    PERSISTENCE LAYER                            │
│              (Local File System - brain/ directory)             │
│  • vectors/: Chroma vector database                            │
│  • facts/: SQLite database                                     │
│  • conversations/: JSON session files                          │
│  • training_data/: Domain-specific knowledge                  │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Core Inference Layer (`assistant/core/`)

#### LLMClient (llm_client.py)
- **Purpose**: Interface with local Ollama server
- **Responsibilities**:
  - Generate text completions
  - Handle streaming responses
  - Parameter management (temp, top_p, max_tokens)
  - Connection pooling and error handling

```
User Query
    ↓
LLMClient.generate()
    ├─ Build message context
    ├─ Format system prompt
    ├─ POST to http://localhost:11434/api/chat
    ├─ Handle streaming/non-streaming
    └─ Return response text
```

**Key Features**:
- Automatically detects Ollama availability
- Fallback error messages if disconnected
- Streaming support for real-time output
- Configurable inference parameters

#### EmbeddingEngine (embedding_engine.py)
- **Purpose**: Generate semantic embeddings locally
- **Responsibilities**:
  - Load sentence-transformer model
  - Batch encode texts to vectors
  - Compute similarity between texts
  - Vector normalization

```
Text Input
    ↓
SentenceTransformer Model
    ├─ Tokenization
    ├─ Forward pass
    ├─ Mean pooling
    └─ L2 normalization
    ↓
[384-dim embedding vector]
```

**Architecture**:
- Model: `all-MiniLM-L6-v2` (384-dim, 22M params)
- Device: CUDA (GPU) or CPU
- Batch processing for efficiency
- Similarity metrics: cosine distance

#### ReasoningEngine (reasoning.py)
- **Purpose**: Implement chain-of-thought reasoning
- **Responsibilities**:
  - Structure step-by-step thinking
  - Extract key facts from reasoning
  - Evaluate relevance of memory items

```
Query + Context
    ↓
Prompt: "Think step-by-step"
    ├─ What is being asked?
    ├─ What relevant knowledge do I have?
    ├─ What approach should I take?
    ├─ What is the analysis?
    └─ What facts should I remember?
    ↓
Parse response sections
    ├─ THINKING
    ├─ ANALYSIS
    ├─ ANSWER
    └─ FACTS_TO_REMEMBER
```

**Output Structure**:
```python
{
    'thinking': str,           # Step-by-step reasoning
    'analysis': str,           # Detailed analysis
    'answer': str,            # Final answer
    'facts_to_store': List    # Extracted facts
}
```

### 2. Memory System (`assistant/memory/`)

#### VectorStore (vector_store.py) - Semantic Memory
- **Database**: Chroma (DuckDB backend)
- **Purpose**: Semantic similarity search
- **Data**: Text embeddings + metadata

```
┌─────────────────────────────────────┐
│     Semantic Memory (Vector DB)     │
├─────────────────────────────────────┤
│ ID  │ Text        │ Embedding  │    │
├─────┼─────────────┼────────────┤    │
│ 1   │ "QBCore..." │ [0.1,...]  │    │
│ 2   │ "Job sys.." │ [0.2,...]  │    │
│ ... │ ...         │ ...        │    │
└─────────────────────────────────────┘

Search:
Query → Embedding → HNSW KNN → Top-K Results
```

**Features**:
- HNSW indexing for fast search
- Cosine distance metric
- Metadata tagging (source, type, timestamp)
- Persistence to disk

**Retrieval Logic**:
```python
1. Embed query text
2. Search Chroma with HNSW
3. Get top-K results
4. Filter by similarity_threshold (default 0.6)
5. Sort by relevance
6. Return with metadata
```

#### FactStore (fact_store.py) - Structured Memory
- **Database**: SQLite
- **Purpose**: Store structured knowledge
- **Schema**:
  - `facts`: Subject-Predicate-Object triples
  - `preferences`: User preferences (key-value)
  - `projects`: Code project metadata
  - `interactions`: Query-response logs

```
FACTS TABLE:
┌────┬─────────┬──────────┬────────┬────────────┐
│ id │ subject │predicate │ object │confidence  │
├────┼─────────┼──────────┼────────┼────────────┤
│ 1  │QBCore   │uses      │Lua     │ 1.0        │
│ 2  │FiveM    │supports  │Lua     │ 1.0        │
└────┴─────────┴──────────┴────────┴────────────┘

PREFERENCES TABLE:
┌────┬─────────┬────────┬──────────────┐
│ id │ key     │ value  │ timestamp    │
├────┼─────────┼────────┼──────────────┤
│ 1  │framework│QBCore  │2024-01-15... │
└────┴─────────┴────────┴──────────────┘
```

#### ConversationHistory (conversation.py)
- **Storage**: JSON files per session
- **Purpose**: Track conversation turns
- **Features**:
  - Timestamp per message
  - Metadata attachment
  - Session management
  - Export functionality

```
SESSION FILE:
[
  {
    "role": "user",
    "content": "How do I create a job?",
    "timestamp": "2024-01-15T10:30:00",
    "metadata": {}
  },
  {
    "role": "assistant",
    "content": "To create a job in QBCore...",
    "timestamp": "2024-01-15T10:30:05",
    "metadata": {"domain": "fivem"}
  }
]
```

#### MemoryManager (memory_manager.py) - Orchestration
- **Purpose**: Unified memory interface
- **Responsibilities**:
  - Coordinate all memory systems
  - Implement RAG pipeline
  - Extract facts from responses
  - Update all memory after successful responses

```
MEMORY UPDATE FLOW:
User Query
    ↓
MemoryManager.retrieve_context()
    ├─ Vector similarity search (top-5)
    ├─ Fact lookup (by keywords)
    ├─ Recent conversation context
    └─ Combine and format
    ↓
[Combined Context String]

Response Generated
    ↓
MemoryManager.update_from_response()
    ├─ Extract facts (regex patterns)
    ├─ Store facts in SQLite
    ├─ Store Q&A pair in vector DB
    ├─ Add to conversation history
    └─ Log interaction for learning
    ↓
Memory Updated
```

### 3. Tools Layer (`assistant/tools/`)

#### FileTool (file_tools.py) - Permission-Based File Access
- **Purpose**: Safe file operations with access control
- **Features**:
  - Whitelist-based directory restrictions
  - Operation-based permissions (read/create/edit/delete)
  - Confirmation for destructive ops
  - Audit trail (logging)

```
FileTool.read(filepath)
    ├─ Check permission
    │   └─ Is filepath in allowed dirs? 
    ├─ Check existence
    ├─ Read with encoding handling
    └─ Return content

FileTool.delete(filepath, ask_confirmation=True)
    ├─ Check permission
    ├─ If requires confirmation:
    │   └─ Prompt user
    ├─ If confirmed:
    │   └─ Delete file
    └─ Log operation
```

**Access Control**:
```yaml
allowed_directories:
  - "./workspace"      # User projects
  - "./brain"         # Memory storage

require_confirmation:
  - "delete"
  - "edit_config"
```

#### CodeAnalyzer (code_analyzer.py) - Code Understanding
- **Purpose**: Extract knowledge from code
- **Supports**: Python, Lua, JavaScript, C/C++

```
ANALYSIS PIPELINE:
Code File
    ├─ Extract functions/classes
    ├─ Find imports/dependencies
    ├─ Extract comments as knowledge
    ├─ Identify patterns (TODO, FIXME, NOTE)
    └─ Build semantic representation
    ↓
{
  'functions': [...],
  'classes': [...],
  'imports': [...],
  'knowledge': [...]
}
```

**Project Analysis**:
```
Directory
    ├─ Scan all code files
    ├─ Group by type
    ├─ Analyze directory structure
    ├─ Extract patterns per language
    └─ Build project semantic map
```

#### MemoryTool (memory_tools.py) - Memory Operations
- **Purpose**: User-facing memory API
- **Operations**:
  - Learn from text
  - Store preferences
  - Store projects
  - Recall memories
  - Forget specific memories
  - Export all memories

### 4. Specialization Layer (`assistant/specialization/`)

#### Knowledge Bases
Each domain has:
- **SYSTEM_PROMPT**: How to behave in this domain
- **KNOWLEDGE_BASE**: Static knowledge (patterns, tips, best practices)

**FiveM Knowledge Base**:
```
├─ Frameworks (QBCore, ESX, RedM)
├─ Common patterns (callbacks, database, commands)
├─ Optimization tips
└─ Security guidelines
```

**MTA Knowledge Base**:
```
├─ Core concepts (resources, events, elements)
├─ Code patterns (server-client sync, database)
├─ Optimization techniques
└─ Best practices
```

**Design Patterns**:
```
├─ UI/UX principles (minimalism, hierarchy)
├─ Architecture patterns (MVC, Observer, Factory)
├─ Code quality (DRY, SOLID, naming)
└─ Documentation standards
```

#### SpecializationLoader (loader.py)
- **Purpose**: Domain selection and context injection
- **Features**:
  - Auto-detect domain from query
  - Format context for specialization
  - Load custom training data
  - Manage multiple knowledge bases

```
DOMAIN DETECTION:
Query contains "qbcore/fivem/gta"? → fivem
Query contains "mta/san andreas"?  → mta
Query contains "design/ui"?         → design
Query contains "code/function"?     → programming
Otherwise                           → general

CONTEXT FORMATTING:
[System Prompt for Domain]
[Relevant Knowledge Snippets]
[User Query]
→ LLM responds with domain expertise
```

### 5. Main Interface (`assistant/main.py`)

#### LocalAIAssistant - Orchestrator
- **Purpose**: Main user-facing class
- **Core Methods**:
  - `chat()`: Full conversation pipeline
  - `learn_from_file()`: Code analysis
  - `learn_from_project()`: Project learning
  - `remember_preference()`: Store preferences
  - `memory_status()`: Get stats
  - `export_memory()`: Backup

```
CHAT PIPELINE:
1. retrieve_context(query)
   └─ Get memory + conversation
2. get_system_prompt(domain)
   └─ Get specialization guidance
3. reason(query, context)
   └─ Step-by-step thinking
4. generate_response()
   └─ LLM inference
5. update_memory()
   └─ Store learning
6. return response

Total: ~5-10 seconds per query
(Depends on model size, GPU availability)
```

## Data Flow Diagrams

### Conversation Flow
```
User Input
    ↓ (CLI/API)
LocalAIAssistant.chat()
    ├─ Detect domain (FiveM? MTA? General?)
    ├─ Retrieve context:
    │   ├─ Vector search (top-5 memories)
    │   ├─ Fact lookup (keywords)
    │   └─ Recent conversation (last 20 msgs)
    ├─ Get specialization system prompt
    ├─ Chain-of-thought reasoning:
    │   ├─ What's being asked?
    │   ├─ Relevant knowledge?
    │   ├─ Step-by-step approach?
    │   └─ Extract facts
    ├─ LLM inference (Ollama):
    │   ├─ System prompt + context
    │   ├─ Generate response
    │   └─ Stream/return text
    ├─ Update memory:
    │   ├─ Extract facts from response
    │   ├─ Store in vector DB
    │   ├─ Add to SQLite facts
    │   └─ Log conversation
    └─ Return to user

Response
    ↓
User sees answer + reasoning (if verbose)
```

### Memory Update Flow
```
Successful Response Generated
    ↓
Extract Facts:
├─ Regex patterns for sentences
├─ Look for "is", "has", "enables" relationships
├─ Confidence scores
    ↓
Store Facts:
├─ SQLite (structured knowledge)
├─ Vector DB (semantic + Q&A pair)
└─ Log interaction (learning data)
    ↓
Memory Updated
    (Future queries will use this knowledge)
```

### RAG Pipeline
```
Query: "How do I optimize FiveM jobs?"
    ↓
Embed Query
    ├─ Sentence transformer
    └─ 384-dim vector
    ↓
Search Vector DB
    ├─ HNSW similarity search
    ├─ Top-5 most similar memories
    └─ Filter by threshold (0.6)
    ↓
Get Matching Memories:
├─ "QBCore job structure..."
├─ "Database optimization tips..."
├─ "FiveM callback patterns..."
└─ "Recent conversation context..."
    ↓
Combine into Context String
    ├─ Memories with scores
    ├─ Relevant facts
    └─ Recent conversation
    ↓
Inject into Prompt:
[System Prompt]
[Retrieved Context]
[User Query]
    ↓
LLM Inference
    └─ Response uses memory context
```

## Performance Characteristics

### Inference Speed (on RTX 4070, 16GB RAM)
- **Model Load**: ~2 seconds (one-time)
- **Ollama Inference**: ~1-3 seconds per 100 tokens
- **Embedding Generation**: ~50ms per text
- **Vector Search**: ~10ms for 1000+ vectors
- **SQLite Query**: ~1ms per fact lookup
- **Full Chat Cycle**: ~5-10 seconds

### Memory Usage
- **Base System**: ~2GB (Python + models loaded)
- **Per Vector Memory**: ~1KB (embedding + metadata)
- **Per Fact**: ~500B (SQLite row)
- **Conversation History**: ~100B per message
- **Typical After 100 Interactions**: 5-8GB total

### Scalability
- **Vectors**: Chroma handles 100k+ efficiently
- **Facts**: SQLite handles 1M+ facts
- **Conversation**: JSON files handle 10k+ messages
- **File Size Limits**: 50MB max per file read (configurable)

## Security Architecture

### Data Isolation
```
User Data (brain/)
├─ Local only (no cloud sync)
├─ AES-256 encryption (optional, future)
├─ No external network calls
└─ Full user control
```

### Permission Model
```
File Access Request
    ├─ Check against whitelist
    │   └─ Only ./workspace and ./brain allowed
    ├─ Check operation type
    │   └─ Is operation permitted?
    ├─ Check confirmation needs
    │   └─ Does user need to confirm?
    └─ Execute or deny
```

### Audit Trail
```
All Operations Logged:
├─ File operations (read/write/delete)
├─ Memory updates
├─ Query results
├─ Fact extractions
└─ User preferences (in interactions table)
```

## Extension Points

### Add New Specialization
1. Create class in `specialization/`
2. Define SYSTEM_PROMPT and KNOWLEDGE_BASE
3. Register in SpecializationLoader.DOMAINS
4. Add training data to `brain/training_data/{domain}/`

### Add New Tools
1. Create in `tools/`
2. Implement required interface
3. Register in LocalAIAssistant.__init__
4. Use in chat() or as standalone

### Custom Memory Systems
1. Implement interface matching VectorStore/FactStore
2. Register in MemoryManager
3. Update retrieval logic
4. Persist to `brain/`

## Future Enhancements

### Short Term
- [ ] Memory summarization (reduce vector store size)
- [ ] Fact importance ranking
- [ ] Conversation pruning (keep important sessions)
- [ ] Performance profiling hooks

### Medium Term
- [ ] Fine-tuning on custom data
- [ ] Advanced RAG (reranking, fusion)
- [ ] Multi-modal learning (images, video)
- [ ] Voice I/O (Whisper integration)

### Long Term
- [ ] Web UI (VS Code-like)
- [ ] Distributed memory (multiple machines)
- [ ] Knowledge graph visualization
- [ ] Automated training data generation

---

**This architecture prioritizes**:
- **Privacy**: Local-first, no external APIs
- **Performance**: Efficient indexing and retrieval
- **Learning**: Automatic fact extraction and storage
- **Extensibility**: Modular design for customization
- **Reliability**: Error handling and audit trails
