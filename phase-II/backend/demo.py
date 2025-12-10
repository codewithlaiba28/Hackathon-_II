#!/usr/bin/env python3
"""
Enhanced Todo Application - Demo Script

This script demonstrates the enhanced UI features of the Todo application.
It can be used to showcase the application at hackathons or for quick demonstrations.
"""

import subprocess
import sys
import time
from pathlib import Path

def run_demo():
    """Run a demonstration of the enhanced Todo application."""
    print("🚀 Enhanced Todo Application Demo")
    print("=" * 50)
    print()

    print("📋 Adding some sample tasks...")
    print("Commands to run:")
    print("  python src/main.py")
    print("  add 'Prepare presentation' 'Create slides for the demo'")
    print("  add 'Practice speech' 'Rehearse the presentation'")
    print("  add 'Gather feedback' 'Collect feedback from team'")
    print("  add 'Submit project' 'Final submission to judges'")
    print()

    print("📊 Viewing all tasks with enhanced table...")
    print("  list")
    print()

    print("✅ Toggling task completion with visual feedback...")
    print("  toggle 1")
    print("  toggle 2")
    print()

    print("🎨 Exporting to professional HTML preview...")
    print("  export_html")
    print()

    print("💡 Other available commands:")
    print("  show - Show all tasks (alias for list)")
    print("  update <id> [new_title] [new_description] - Update a task")
    print("  delete <id> - Delete a task")
    print("  dashboard - Show task summary dashboard")
    print("  help - Show all commands")
    print("  exit - Exit the application")
    print()

    print("✨ Enhanced UI Features:")
    print("  • Rounded borders in task tables")
    print("  • Alternating row styles")
    print("  • Strikethrough for completed tasks")
    print("  • Color-coded status (yellow=Pending, green=Complete)")
    print("  • Professional panels for messages")
    print("  • Modern HTML export with CSS styling")
    print()

    print("🎯 To run the demo yourself:")
    print("  1. Run: python src/main.py")
    print("  2. Try the commands above")
    print("  3. Check the generated preview.html file")
    print()

    print("🚀 Happy hacking!")

def run_interactive_demo():
    """Start the actual application for interactive demo."""
    print("Starting the Enhanced Todo Application...")
    print("Try these commands in the app:")
    print("  add 'Sample Task' 'This is a sample task description'")
    print("  list")
    print("  toggle 1")
    print("  export_html")
    print()

    try:
        subprocess.run([sys.executable, "src/main.py"], check=True)
    except subprocess.CalledProcessError:
        print("Application exited or was terminated.")
    except KeyboardInterrupt:
        print("\nDemo interrupted by user.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        run_interactive_demo()
    else:
        run_demo()