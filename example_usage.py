#!/usr/bin/env python3
"""
Example usage of LocalAI Assistant with persistent memory.

Before running:
1. Install dependencies: pip install -r requirements.txt
2. Start Ollama: ollama serve
3. Pull a model: ollama pull mistral
"""

from assistant import LocalAIAssistant
import json

def main():
    # Initialize assistant
    assistant = LocalAIAssistant()

    # Example 1: Basic chat with memory
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Chat with Memory Persistence")
    print("="*70)

    result = assistant.chat(
        "I'm working on a FiveM QBCore job system. How should I structure it?",
        domain="fivem",
        verbose=True
    )

    print(f"\n🤖 Assistant: {result['response']}")
    print(f"\n💭 Thinking: {result['thinking']}")
    print(f"📚 Learned facts: {result['facts_learned']}")

    # Example 2: Learn from file
    print("\n" + "="*70)
    print("EXAMPLE 2: Learn from Code File")
    print("="*70)

    # Create example FiveM code
    example_code = """
-- FiveM Job System
local QBCore = exports['qb-core']:GetCoreObject()

local Jobs = {
    police = {
        label = 'Police',
        grades = {
            {name = 'recruit', payment = 100}
        }
    },
    mechanic = {
        label = 'Mechanic',
        grades = {
            {name = 'apprentice', payment = 75}
        }
    }
}

-- Set player job
function SetPlayerJob(player, job)
    local Player = QBCore.Functions.GetPlayer(player)
    Player.Functions.SetJob(job, 1)
end

-- Get job info
function GetJobInfo(job)
    return Jobs[job]
end
"""

    import tempfile
    import os

    with tempfile.NamedTemporaryFile(mode='w', suffix='.lua', delete=False) as f:
        f.write(example_code)
        temp_file = f.name

    try:
        learn_result = assistant.learn_from_file(temp_file)
        print(f"✅ Analyzed file:")
        print(f"  - Language: {learn_result['analysis']['language']}")
        print(f"  - Functions found: {learn_result['analysis'].get('functions', [])}")
        print(f"  - Facts extracted: {len(learn_result['facts_extracted'])}")
    finally:
        os.unlink(temp_file)

    # Example 3: Store and retrieve preferences
    print("\n" + "="*70)
    print("EXAMPLE 3: User Preferences with Memory")
    print("="*70)

    assistant.remember_preference("primary_language", "Lua")
    assistant.remember_preference("fivem_framework", "QBCore")
    assistant.remember_preference("code_style", "minimalist")

    print("Stored preferences:")
    print(f"  Primary Language: {assistant.get_preference('primary_language')}")
    print(f"  FiveM Framework: {assistant.get_preference('fivem_framework')}")
    print(f"  Code Style: {assistant.get_preference('code_style')}")

    # Example 4: Domain-specific chat
    print("\n" + "="*70)
    print("EXAMPLE 4: Domain-Specific Expertise")
    print("="*70)

    domains = ["fivem", "mta", "design"]

    for domain in domains:
        result = assistant.chat(
            f"What are the best practices for {domain}?",
            domain=domain
        )
        print(f"\n{domain.upper()}: {result['response'][:200]}...")

    # Example 5: Memory statistics
    print("\n" + "="*70)
    print("EXAMPLE 5: Memory Statistics")
    print("="*70)

    stats = assistant.memory_status()
    print(json.dumps(stats, indent=2))

    # Example 6: Multi-turn conversation
    print("\n" + "="*70)
    print("EXAMPLE 6: Multi-Turn Conversation")
    print("="*70)

    queries = [
        ("What's the difference between ESX and QBCore?", "fivem"),
        ("Can you explain the payment systems?", "fivem"),
        ("How would you implement this in MTA instead?", "mta")
    ]

    for query, domain in queries:
        result = assistant.chat(query, domain=domain)
        print(f"\nQ: {query}")
        print(f"A: {result['response'][:300]}...")
        print(f"   (Memory context used: {result['memory_context_used']} lines)")

    # Example 7: Export memory
    print("\n" + "="*70)
    print("EXAMPLE 7: Export Memory")
    print("="*70)

    assistant.export_memory("./memory_backup")
    print("✅ Memory exported to ./memory_backup")

    # Final status
    print("\n" + "="*70)
    print("FINAL STATUS")
    print("="*70)
    assistant.memory_status()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
