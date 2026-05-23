#!/usr/bin/env python3
"""
Interactive CLI for LocalAI Assistant.

Commands:
  /chat <query>          - Chat with the assistant
  /domain <domain>       - Set current domain (fivem, mta, design, programming)
  /learn <filepath>      - Learn from a code file
  /project <path>        - Learn from a project directory
  /memory                - Show memory statistics
  /forget                - Clear all memories
  /export <path>         - Export memories
  /pref <key> <value>    - Store a preference
  /recall <key>          - Get a preference
  /help                  - Show commands
  /exit                  - Exit the program
"""

from assistant import LocalAIAssistant
import os
import sys

class CLIInterface:
    def __init__(self):
        self.assistant = LocalAIAssistant()
        self.current_domain = "general"
        self.verbose = False

    def print_banner(self):
        print("""
╔══════════════════════════════════════════════════════════════════╗
║           🤖 LocalAI Assistant - Persistent Memory              ║
║                                                                  ║
║  Fully local. No cloud APIs. Learns from every interaction.     ║
║  Type /help for commands or /exit to quit.                     ║
╚══════════════════════════════════════════════════════════════════╝
        """)

    def parse_command(self, user_input: str):
        """Parse and execute user commands."""

        if not user_input.strip():
            return

        parts = user_input.strip().split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if command == "/chat" or (not command.startswith("/") and self.current_domain != "general"):
            self.cmd_chat(user_input if not command.startswith("/") else args)

        elif command == "/domain":
            self.cmd_domain(args)

        elif command == "/learn":
            self.cmd_learn(args)

        elif command == "/project":
            self.cmd_project(args)

        elif command == "/memory":
            self.cmd_memory()

        elif command == "/forget":
            self.cmd_forget()

        elif command == "/export":
            self.cmd_export(args)

        elif command == "/pref":
            self.cmd_pref(args)

        elif command == "/recall":
            self.cmd_recall(args)

        elif command == "/verbose":
            self.cmd_verbose()

        elif command == "/help":
            self.cmd_help()

        elif command == "/exit":
            self.cmd_exit()

        else:
            # Treat as chat if not a command
            if command.startswith("/"):
                print("❌ Unknown command. Type /help for available commands.")
            else:
                self.cmd_chat(user_input)

    def cmd_chat(self, query: str):
        """Process chat query."""
        if not query.strip():
            print("❌ Please provide a query.")
            return

        result = self.assistant.chat(
            query,
            domain=self.current_domain,
            verbose=self.verbose
        )

        print(f"\n{'='*70}")
        print(f"🤖 RESPONSE (Domain: {result['domain'].upper()})")
        print(f"{'='*70}")
        print(result['response'])

        if self.verbose and result['thinking']:
            print(f"\n💭 THINKING:\n{result['thinking']}")

        if result['facts_learned']:
            print(f"\n📚 FACTS LEARNED: {', '.join(result['facts_learned'][:3])}")

        print(f"{'='*70}\n")

    def cmd_domain(self, domain: str):
        """Set current specialization domain."""
        if not domain.strip():
            print(f"Current domain: {self.current_domain}")
            available = self.assistant.specialization.get_available_domains()
            print(f"Available: {', '.join(available)}")
            return

        domain = domain.strip().lower()
        if domain in self.assistant.specialization.get_available_domains():
            self.current_domain = domain
            print(f"✅ Domain set to: {domain}")
        else:
            print(f"❌ Unknown domain. Available: {', '.join(self.assistant.specialization.get_available_domains())}")

    def cmd_learn(self, filepath: str):
        """Learn from a code file."""
        if not filepath.strip():
            print("❌ Please provide a file path.")
            return

        filepath = filepath.strip()
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return

        result = self.assistant.learn_from_file(filepath)

        if 'error' in result:
            print(f"❌ {result['error']}")
        else:
            print(f"✅ Learned from {filepath}")
            print(f"   - Facts extracted: {result['stored_count']}")
            print(f"   - Language: {result['analysis'].get('language', 'Unknown')}")

    def cmd_project(self, project_path: str):
        """Learn from a project directory."""
        if not project_path.strip():
            print("❌ Please provide a directory path.")
            return

        project_path = project_path.strip()
        if not os.path.isdir(project_path):
            print(f"❌ Directory not found: {project_path}")
            return

        result = self.assistant.learn_from_project(project_path)

        if 'error' in result:
            print(f"❌ {result['error']}")
        else:
            print(f"✅ Learned from project: {result['project']}")
            print(f"   - Files analyzed: {result['files_analyzed']}")
            print(f"   - Facts extracted: {result['facts_extracted']}")
            print(f"   - Language: {result.get('structure', {}).get('subdirs', [])}")

    def cmd_memory(self):
        """Show memory statistics."""
        print("\n" + "="*70)
        print("📊 MEMORY STATISTICS")
        print("="*70)

        stats = self.assistant.memory_status()

        vs = stats['vector_store']
        fs = stats['fact_store']
        conv = stats['conversation']

        print(f"\n📝 VECTOR STORE (Semantic Memories)")
        print(f"   Total memories: {vs.get('total_memories', 0)}")

        print(f"\n📚 FACT STORE")
        print(f"   Facts: {fs.get('facts', 0)}")
        print(f"   Preferences: {fs.get('preferences', 0)}")
        print(f"   Projects known: {fs.get('projects', 0)}")
        print(f"   Interactions logged: {fs.get('interactions', 0)}")

        print(f"\n💬 CONVERSATION")
        print(f"   Total messages: {conv.get('total_messages', 0)}")
        print(f"   User messages: {conv.get('user_messages', 0)}")
        print(f"   Assistant messages: {conv.get('assistant_messages', 0)}")
        print(f"   Session: {conv.get('session_file', 'N/A')}")

        print("="*70 + "\n")

    def cmd_forget(self):
        """Clear all memories."""
        response = input("⚠️  This will DELETE ALL MEMORIES. Type 'YES' to confirm: ")
        if response == "YES":
            self.assistant.clear_memory(confirm=True)
            print("✅ Memory cleared.")
        else:
            print("Cancelled.")

    def cmd_export(self, path: str):
        """Export memories to directory."""
        if not path.strip():
            path = "./memory_export"

        path = path.strip()

        try:
            self.assistant.export_memory(path)
            print(f"✅ Memory exported to {path}")
        except Exception as e:
            print(f"❌ Export failed: {e}")

    def cmd_pref(self, args: str):
        """Store preference."""
        parts = args.strip().split(maxsplit=1)
        if len(parts) < 2:
            print("❌ Usage: /pref <key> <value>")
            return

        key, value = parts[0], parts[1]
        self.assistant.remember_preference(key, value)
        print(f"✅ Stored: {key} = {value}")

    def cmd_recall(self, key: str):
        """Retrieve preference."""
        if not key.strip():
            print("❌ Usage: /recall <key>")
            return

        value = self.assistant.get_preference(key.strip())
        if value:
            print(f"💾 {key} = {value}")
        else:
            print(f"❌ Preference not found: {key}")

    def cmd_verbose(self):
        """Toggle verbose mode."""
        self.verbose = not self.verbose
        status = "ON" if self.verbose else "OFF"
        print(f"✅ Verbose mode: {status}")

    def cmd_help(self):
        """Show help."""
        help_text = """
COMMANDS:
  Direct chat (no prefix): Type your query directly
  /chat <query>           - Chat with specific query
  /domain <name>          - Set specialization (fivem, mta, design, programming)
  /learn <filepath>       - Learn from a code file
  /project <path>         - Learn from entire project
  /memory                 - Show memory statistics
  /pref <key> <value>     - Store a preference
  /recall <key>           - Get a preference
  /export [path]          - Export memories (default: ./memory_export)
  /forget                 - Clear all memories (requires confirmation)
  /verbose                - Toggle verbose mode (show thinking)
  /help                   - This help message
  /exit                   - Exit the program

EXAMPLES:
  How do I set up a QBCore job system?
  /domain fivem
  /learn ./jobs/police.lua
  /pref framework QBCore
  /recall framework
"""
        print(help_text)

    def cmd_exit(self):
        """Exit program."""
        print("\n👋 Goodbye! Your memories are safely stored locally.")
        sys.exit(0)

    def run(self):
        """Run interactive CLI."""
        self.print_banner()

        while True:
            try:
                domain_indicator = f"[{self.current_domain.upper()}]" if self.current_domain != "general" else ""
                prompt = f"You {domain_indicator}> "
                user_input = input(prompt).strip()

                if user_input:
                    self.parse_command(user_input)

            except KeyboardInterrupt:
                print("\n\n^C")
                self.cmd_exit()
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    cli = CLIInterface()
    cli.run()

if __name__ == "__main__":
    main()
