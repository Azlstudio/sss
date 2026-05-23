# 💡 LocalAI Assistant - Practical Usage Guide

Real-world examples and patterns for using the LocalAI Assistant effectively.

## Table of Contents
- [Basic Chat](#basic-chat)
- [Learning from Code](#learning-from-code)
- [Domain-Specific Workflows](#domain-specific-workflows)
- [Memory Management](#memory-management)
- [Advanced Patterns](#advanced-patterns)

---

## Basic Chat

### Starting the Assistant

```bash
python cli.py
```

You'll see:
```
╔══════════════════════════════════════════════════════════════════╗
║           🤖 LocalAI Assistant - Persistent Memory              ║
║                                                                  ║
║  Fully local. No cloud APIs. Learns from every interaction.     ║
║  Type /help for commands or /exit to quit.                     ║
╚══════════════════════════════════════════════════════════════════╝

You> 
```

### Simple Questions

```
You> How do I use loops in Lua?

🤔 Processing: How do I use loops in Lua?
================================================
🤖 RESPONSE (Domain: PROGRAMMING)
================================================

In Lua, you have several loop constructs:

1. For Loop (numeric):
   for i = 1, 10 do
       print(i)
   end

2. For-in Loop (iterator):
   for k, v in pairs(table) do
       print(k, v)
   end

3. While Loop:
   while condition do
       -- code
   end

4. Repeat-Until Loop:
   repeat
       -- code
   until condition
   
[Full response with examples...]
================================================
```

### Multi-Turn Conversations

The assistant remembers context across messages:

```
You> What's the main difference between QBCore and ESX?

🤖 RESPONSE
[Detailed comparison...]

You> Which one is easier for beginners?

🤔 Processing: Which one is easier for beginners?

🤖 RESPONSE
Based on what we just discussed about QBCore and ESX...
[Response uses previous context]
```

---

## Learning from Code

### Learn from a Single File

```
You> /learn ./jobs/police.lua

📚 Learning from: ./jobs/police.lua
✅ Learned from ./jobs/police.lua
   - Facts extracted: 5
   - Language: Lua
```

The assistant now knows about:
- Functions defined in the file
- Patterns used
- Comments and documentation
- Import/dependencies

### Learn from an Entire Project

```
You> /project ./my_qbcore_server

📂 Analyzing project: ./my_qbcore_server
✅ Learned from 12 files, extracted 47 facts

The assistant now understands:
- Project structure
- File organization
- Common patterns used
- Dependencies between modules
```

### Check What It Learned

```
You> /memory

📊 MEMORY STATISTICS
================================================
📝 VECTOR STORE (Semantic Memories)
   Total memories: 143

📚 FACT STORE
   Facts: 87
   Preferences: 3
   Projects known: 2
   Interactions logged: 24

💬 CONVERSATION
   Total messages: 48
   User messages: 24
   Assistant messages: 24
   Session: ./brain/conversations/session_...

================================================
```

---

## Domain-Specific Workflows

### FiveM Development Workflow

#### Step 1: Set Domain
```
You> /domain fivem
✅ Domain set to: fivem
```

#### Step 2: Get Framework-Specific Help
```
You> How do I create a callback in QBCore?

🤖 RESPONSE (Domain: FIVEM)
================================================

To create a callback in QBCore:

Server-side callback registration:
exports['qb-core']:CreateCallback('GetPlayerData', function(source, cb)
    local Player = QBCore.Functions.GetPlayer(source)
    cb(Player.PlayerData)
end)

Client-side callback request:
QBCore.Functions.TriggerCallback('GetPlayerData', function(data)
    print(json.encode(data))
end)

[Full explanation with best practices...]
```

#### Step 3: Learn Your Code
```
You> /learn ./resources/jobs/police.lua
✅ Learned from file
   Functions found: ['SetPlayerJob', 'GetJobGrade']
   Facts extracted: 8

You> Now explain how my police job system works

🤖 RESPONSE (Domain: FIVEM)
Based on analyzing your police.lua file:

Your job system:
- Uses QBCore job framework
- Has 3 grade levels
- Stores data in database
- Implements callbacks for sync
- [Detailed analysis of YOUR code]
```

#### Step 4: Store Preferences
```
You> /pref framework QBCore
💾 Remembered: framework = QBCore

You> /pref primary_language Lua
💾 Remembered: primary_language = Lua

Now the assistant remembers your preferences and defaults to FiveM domain.
```

### MTA Development Workflow

```
You> /domain mta
✅ Domain set to: mta

You> How do I handle client-server communication?

🤖 RESPONSE (Domain: MTA)
================================================

In MTA, client-server communication uses events:

Server to Client:
triggerClientEvent(player, 'eventName', sourceResource, arg1, arg2)

Client to Server:
triggerServerEvent('eventName', arg1, arg2)

Client-side listener:
addEventHandler('eventName', resourceRoot, function(arg1, arg2)
    -- handle event
end)

[Full guide with patterns...]
```

### Design/UX Questions

```
You> /domain design
✅ Domain set to: design

You> What are the principles of minimalist design?

🤖 RESPONSE (Domain: DESIGN)
================================================

Minimalism in design focuses on:

1. Remove Unnecessary Elements
   - Keep only essential information
   - Use whitespace effectively
   
2. Focus User Attention
   - Clear visual hierarchy
   - Emphasis on primary actions
   
3. Simplicity
   - Limited color palette (2-3 main + accents)
   - Clear typography (1-2 fonts)
   - Consistent spacing
   
[Complete guide with examples...]
```

---

## Memory Management

### Store Preferences

```
You> /pref favorite_framework QBCore
💾 Remembered: favorite_framework = QBCore

You> /pref code_style minimalist
💾 Remembered: code_style = minimalist

You> /pref use_oxmysql yes
💾 Remembered: use_oxmysql = yes
```

### Recall Preferences

```
You> /recall favorite_framework
💾 favorite_framework = QBCore

You> /recall code_style
💾 code_style = minimalist
```

### Store Project Metadata

```
You> /learn ./my_police_job
📚 Learning from: ./my_police_job
✅ Learned from 8 files

You> Remember, this is my police job system for QBCore servers

🤖 Understood. I'll remember this project structure.

Later:
You> Show me the pattern in my police job system

🤖 Based on your police job project:
[Shows patterns from your learned code]
```

### Export Your Memory

```
You> /export ./my_memory_backup
📤 Memory exported to ./my_memory_backup

Files created:
├─ vector_memories.json    # All learned knowledge
├─ conversation.json       # Chat history
└─ conversation.txt        # Human-readable format
```

### Clear Memory (Be Careful!)

```
You> /forget
⚠️  This will DELETE ALL MEMORIES. Type 'YES' to confirm: YES
🗑️  All memory cleared.
```

---

## Advanced Patterns

### Teaching the Assistant Your Coding Style

```
You> /learn ./my_best_project.lua

You> /domain fivem

You> Based on my code style, what are my preferred patterns?

🤖 RESPONSE
From analyzing your code, I see you prefer:
- Modular structure with separate files
- Object-oriented patterns
- Comprehensive error handling
- Clear variable naming
- [Analysis of your actual style]

I'll use these patterns in future code suggestions.
```

### Cross-Domain Learning

```
You> /domain fivem
You> /learn ./server.lua
✅ Learned 15 facts about FiveM patterns

You> /domain design
You> Now, how should I structure my UI based on minimalist design?

🤖 RESPONSE
Combining FiveM knowledge with design principles:
- Your server uses callback patterns → Use event-based UI updates
- Your code is modular → Organize UI components separately
- Based on minimalist design → Limit UI elements to essential
[Integrated response using both domains]
```

### Using Chat History for Context

```
You> I'm building a job system

You> What's the best database structure?

You> How do I sync this with the client?

You> Show me code examples

Each response builds on previous context. The assistant remembers:
- What system you're building (job system)
- Previous answers (database structure)
- Questions asked (client sync)
```

### Creating Custom Training Data

```
1. Create directory:
   mkdir -p brain/training_data/my_framework

2. Add your docs:
   brain/training_data/my_framework/
   ├─ getting_started.md
   ├─ best_practices.md
   └─ code_patterns.lua

3. Load automatically on next startup

4. Use in queries:
   You> Explain my_framework patterns
   🤖 RESPONSE uses your custom training data
```

---

## Performance Tips

### Faster Responses

```
# Use smaller model (faster)
config.yaml:
  model: "neural-chat"  # instead of mistral

# Reduce token limit
  max_tokens: 1024      # instead of 2048

# Use CPU embedding (if needed)
  device: "cpu"
```

### Better Memory Retrieval

```
# Check what's being retrieved
You> /verbose
✅ Verbose mode: ON

Now responses show:
- What memories were found
- Similarity scores
- Facts used
- Thinking process

# This helps you understand if relevant knowledge is being retrieved
```

### Manage Growing Memory

```
# Monitor memory size
You> /memory
[Shows statistics]

# Export and prune if needed
You> /export ./backup
You> /forget
[Clear and reload from backup or fresh]
```

---

## Common Workflows

### "Teach Me" Pattern

```
You> /domain fivem

You> /learn ./expert_qbcore_resource.lua

You> Explain this resource in detail

You> Show me the job system implementation

You> What are the best practices used here?

🤖 Learns from real code, not just documentation
```

### "Build With Me" Pattern

```
You> /domain fivem

You> I'm building a custom job system

You> What should the database schema look like?

You> /learn ./reference_job.lua

You> Now, how should I modify this for my needs?

You> Generate code for [specific feature]

🤖 Learns from your project, provides tailored suggestions
```

### "Check My Code" Pattern

```
You> /domain fivem

You> /learn ./my_implementation.lua

You> Review my job system for best practices

You> Any security concerns?

You> Performance optimizations?

🤖 Analyzes YOUR code against domain best practices
```

### "Explain Concepts" Pattern

```
You> /domain design

You> What's minimalist design?

You> How do I apply it to a game UI?

You> Show examples in Lua

You> What about accessibility?

🤖 Teaches concepts with domain-specific context
```

---

## Troubleshooting

### Assistant Not Remembering?

```
You> /memory
📊 Check if vector memories exist

You> /domain general
You> /learn ./important_file.lua
Make sure to explicitly teach it
```

### Slow Responses?

```
You> /verbose
[Check what's happening]

Fix:
1. Reduce max_tokens in config.yaml
2. Use smaller model (neural-chat)
3. Close other applications
4. Check /memory size (might need pruning)
```

### Wrong Domain?

```
You> /domain fivem
✅ Domain set to: fivem

The assistant remembers your domain until you change it
```

### Lost Previous Knowledge?

```
You> /export ./my_backup
Backup before experimenting

You> /forget
Clear if needed

Restore:
Backup files still in ./my_backup
Manually load training data as needed
```

---

## Best Practices

### 1. Always Teach Project Context
```
Good:  /learn ./my_full_project
Bad:   Ask questions without teaching first
```

### 2. Use Domains Effectively
```
Good:  /domain fivem, then ask FiveM questions
Bad:   Mix domains without setting context
```

### 3. Store Preferences
```
Good:  /pref framework QBCore, /pref language Lua
Bad:   Repeat same info every time
```

### 4. Backup Important Memory
```
Good:  /export ./backups before major changes
Bad:   /forget without backup
```

### 5. Check Memory Stats
```
Good:  /memory to see what's learned
Bad:   Assume everything is remembered
```

---

## Example Session

```
$ python cli.py

You> /domain fivem
✅ Domain set to: fivem

You> /pref framework QBCore
💾 Remembered: framework = QBCore

You> /learn ./qbcore-jobs/server.lua
✅ Learned from file

You> How do I add a new job?
[Gets QBCore-specific answer using your code]

You> /project ./my_qbcore_resources
✅ Learned from 5 files

You> Explain the pattern used in my resources
[Analyzes YOUR patterns]

You> /memory
[Shows 50 memories, 30 facts, 2 projects]

You> Show me best practices for my code
[Uses stored code + domain expertise]

You> /export ./session_backup
📤 Backed up successfully

You> /help
[Shows all commands]

You> /exit
👋 Goodbye!
```

---

## Summary

The LocalAI Assistant is most powerful when you:
1. **Teach it** your projects and code
2. **Use domains** to focus expertise
3. **Store preferences** for personalization
4. **Export backups** to protect knowledge
5. **Reference past learning** in new queries

Everything stays local, everything is remembered, everything is yours.

Start exploring! 🚀
