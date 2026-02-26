import sys
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from src.services.task_service import TaskService


class TodoCLI:
    """Command-line interface for the todo application."""

    def __init__(self, task_service: TaskService):
        """Initialize the CLI with a task service.

        Args:
            task_service: The task service to use for operations.
        """
        self.task_service = task_service
        self.console = Console()

    def run(self):
        """Start the REPL loop."""
        # Enhanced welcome message with panel
        welcome_text = Text("Welcome to the Todo Application!", style="bold blue")
        welcome_text.append("\n\nType 'help' for available commands or 'exit' to quit.", style="italic")
        self.console.print(Panel(welcome_text, title="Todo App", border_style="blue", expand=False))
        self.console.print()  # Add spacing

        while True:
            try:
                # Get user input with styled prompt
                user_input = input("todo> ").strip()

                if not user_input:
                    continue

                # Parse the command
                parts = user_input.split(' ', 1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""

                # Execute the command
                if command == 'exit':
                    self._exit()
                elif command == 'help':
                    self._help()
                elif command == 'add':
                    self._add(args)
                elif command == 'list':
                    self._list()
                elif command == 'show':
                    self._list()  # show is an alias for list
                elif command == 'update':
                    # Handle 'update <id> [title] [description]' or 'update tasks <id> [title] [description]'
                    if args.startswith('tasks '):
                        # Extract arguments after 'tasks '
                        subcommand_args = args[6:].strip()  # Remove 'tasks ' part
                        self._update(subcommand_args)
                    else:
                        self._update(args)
                elif command == 'delete':
                    self._delete(args)
                elif command == 'toggle':
                    self._toggle(args)
                elif command == 'dashboard':
                    self._dashboard()
                elif command == 'export_html':
                    self._export_html()
                else:
                    error_msg = f"Unknown command: '{command}'. Type 'help' for available commands."
                    self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))
            except KeyboardInterrupt:
                goodbye_text = Text("Goodbye!", style="bold")
                self.console.print(Panel(goodbye_text, border_style="blue", expand=False))
                sys.exit(0)
            except EOFError:
                goodbye_text = Text("Goodbye!", style="bold")
                self.console.print(Panel(goodbye_text, border_style="blue", expand=False))
                sys.exit(0)

    def _exit(self):
        """Exit the application."""
        goodbye_text = Text("Goodbye! Thanks for using the Todo Application.", style="bold green")
        self.console.print(Panel(goodbye_text, border_style="green", expand=False))
        sys.exit(0)

    def _help(self):
        """Display help information."""
        help_text = Text("Available commands:\n", style="bold underline")
        help_text.append("  add <title> [description]  ", style="cyan")
        help_text.append("- Add a new task\n")
        help_text.append("  add <task1>, <task2>, ... ", style="cyan")
        help_text.append("- Add multiple tasks separated by commas\n")
        help_text.append("  list                      ", style="cyan")
        help_text.append("- List all tasks\n")
        help_text.append("  show                      ", style="cyan")
        help_text.append("- Show all tasks (alias for list)\n")
        help_text.append("  update <id> [title] [description] ", style="cyan")
        help_text.append("- Update a task\n")
        help_text.append("  delete <id>               ", style="cyan")
        help_text.append("- Delete a task\n")
        help_text.append("  toggle <id>               ", style="cyan")
        help_text.append("- Toggle task completion status\n")
        help_text.append("  dashboard                 ", style="cyan")
        help_text.append("- Show task summary dashboard\n")
        help_text.append("  export_html               ", style="cyan")
        help_text.append("- Export tasks to HTML\n")
        help_text.append("  help                      ", style="cyan")
        help_text.append("- Show this help message\n")
        help_text.append("  exit                      ", style="cyan")
        help_text.append("- Exit the application")

        self.console.print(Panel(help_text, title="Help", border_style="blue", expand=False))

    def _add(self, args: str):
        """Add a new task or multiple tasks separated by commas.

        Args:
            args: The command arguments containing title and optional description.
        """
        try:
            # Parse title and description from args
            args = args.strip()
            if not args:
                error_msg = "Title is required. Usage: add <title> [description] or add <task1>, <task2>, <task3>"
                self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))
                return

            # Check if we have comma-separated tasks
            if ',' in args:
                # Split by comma and process each task
                # Each comma-separated part should be treated as a complete title
                task_parts = [part.strip() for part in args.split(',')]
                added_tasks = []

                for task_part in task_parts:
                    if not task_part:
                        continue

                    # Each part becomes the title, with empty description
                    title = task_part.strip()
                    description = ""

                    task = self.task_service.add_task(title, description)
                    added_tasks.append(task)

                if added_tasks:
                    success_msg = Text(f"Added {len(added_tasks)} task(s) successfully!", style="green")
                    for task in added_tasks:
                        success_msg.append(f"\nID: {task.id} - {task.title}")
                        if task.description:
                            success_msg.append(f" (Description: {task.description})")
                    self.console.print(Panel(success_msg, title="Success", border_style="green", expand=False))
                else:
                    error_msg = "No valid tasks found to add."
                    self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))
            else:
                # Handle single task - maintain original behavior where first word is title and second word is description
                parts = self._parse_args(args)

                if len(parts) >= 2:
                    # There's a description part (either quoted or unquoted after first word)
                    title = parts[0]
                    description = parts[1] if len(parts) > 1 else ""
                    # If there are more than 2 parts, join the rest as description
                    if len(parts) > 2:
                        description = " ".join(parts[1:])

                    task = self.task_service.add_task(title, description)
                else:
                    # Only a title was provided
                    if parts:
                        title = parts[0]
                        task = self.task_service.add_task(title)
                    else:
                        error_msg = "Title is required. Usage: add <title> [description]"
                        self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))
                        return

                success_msg = Text(f"Task added successfully! ID: {task.id}", style="green")
                success_msg.append(f"\nTitle: {task.title}")
                if task.description:
                    success_msg.append(f"\nDescription: {task.description}")
                self.console.print(Panel(success_msg, title="Success", border_style="green", expand=False))
        except ValueError as e:
            error_msg = f"{str(e)}"
            self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))

    def _list(self):
        """List all tasks."""
        try:
            tasks = self.task_service.list_tasks()

            if not tasks:
                self.console.print(Panel("No tasks found.", title="Info", border_style="yellow", expand=False))
                return

            # Create enhanced table with rounded borders
            table = Table(
                title="Your Tasks",
                title_style="bold blue",
                box=box.ROUNDED,
                header_style="bold magenta",
                border_style="blue",
                row_styles=["none", "dim"]  # Alternating row styles
            )
            table.add_column("ID", style="dim", width=5, justify="center")
            table.add_column("Title", min_width=15)
            table.add_column("Description", min_width=20)
            table.add_column("Status", justify="center")

            for task in tasks:
                # Apply strikethrough for completed tasks
                title_text = Text(task.title)
                if task.status == "Complete":
                    title_text.stylize("strike")

                description_text = Text(task.description)
                if task.status == "Complete":
                    description_text.stylize("dim")

                status_style = "green" if task.status == "Complete" else "yellow"
                status_text = Text(task.status)
                if task.status == "Complete":
                    status_text.stylize("bold green")
                else:
                    status_text.stylize("bold yellow")

                table.add_row(
                    str(task.id),
                    title_text,
                    description_text,
                    status_text
                )

            self.console.print(table)
        except Exception as e:
            error_msg = f"Error listing tasks: {str(e)}"
            self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))

    def _update(self, args: str):
        """Update a task.

        Args:
            args: The command arguments containing task ID and new values.
        """
        try:
            parts = self._parse_args(args)
            if len(parts) < 2:  # Need at least ID and one field to update
                error_msg = "Usage: update <id> [new_title] [new_description]"
                self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))
                return

            try:
                task_id = int(parts[0])
            except ValueError:
                error_msg = "Task ID must be a number"
                self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))
                return

            # Extract new title and description
            new_title = None
            new_description = None

            if len(parts) >= 2:
                new_title = parts[1] if parts[1] != "None" else None
            if len(parts) >= 3:
                new_description = parts[2] if parts[2] != "None" else None

            task = self.task_service.update_task(task_id, new_title, new_description)
            success_msg = Text(f"Task {task_id} updated successfully!", style="green")
            success_msg.append(f"\nNew Title: {task.title}")
            if task.description:
                success_msg.append(f"\nNew Description: {task.description}")
            self.console.print(Panel(success_msg, title="Success", border_style="green", expand=False))
        except ValueError as e:
            error_msg = f"{str(e)}"
            self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))

    def _delete(self, args: str):
        """Delete a task.

        Args:
            args: The command arguments containing task ID.
        """
        try:
            args = args.strip()
            if not args:
                error_msg = "Task ID is required. Usage: delete <id>"
                self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))
                return

            try:
                task_id = int(args)
            except ValueError:
                error_msg = "Task ID must be a number"
                self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))
                return

            success = self.task_service.delete_task(task_id)
            if success:
                success_msg = f"Task {task_id} deleted successfully!"
                self.console.print(Panel(success_msg, title="Success", border_style="green", expand=False))
            else:
                error_msg = f"Task with ID {task_id} does not exist"
                self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))
        except ValueError as e:
            error_msg = f"{str(e)}"
            self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))

    def _toggle(self, args: str):
        """Toggle task completion status.

        Args:
            args: The command arguments containing task ID.
        """
        try:
            args = args.strip()
            if not args:
                error_msg = "Task ID is required. Usage: toggle <id>"
                self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))
                return

            try:
                task_id = int(args)
            except ValueError:
                error_msg = "Task ID must be a number"
                self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))
                return

            task = self.task_service.toggle_task_status(task_id)
            if task:
                status = "Complete" if task.status == "Complete" else "Pending"
                status_style = "bold green" if task.status == "Complete" else "bold yellow"
                success_msg = Text(f"Task {task_id} status toggled to {status}!", style=status_style)
                self.console.print(Panel(success_msg, title="Success", border_style="green", expand=False))
            else:
                error_msg = f"Task with ID {task_id} does not exist"
                self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))
        except ValueError as e:
            error_msg = f"{str(e)}"
            self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))

    def _export_html(self):
        """Export tasks to an HTML file."""
        try:
            tasks = self.task_service.list_tasks()

            html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced Todo Tasks</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f7fa;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .subtitle {
            margin-top: 10px;
            opacity: 0.8;
            font-weight: 300;
        }
        .table-container {
            padding: 30px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }
        th, td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        th {
            background-color: #f8f9fa;
            font-weight: 600;
            color: #555;
            text-transform: uppercase;
            font-size: 0.8em;
            letter-spacing: 0.5px;
        }
        tr:hover {
            background-color: #f8f9fa;
        }
        .complete {
            color: #28a745;
            font-weight: bold;
            background-color: #f8fff9;
        }
        .pending {
            color: #ffc107;
            font-weight: bold;
            background-color: #fffef8;
        }
        .completed-task {
            text-decoration: line-through;
            color: #6c757d;
        }
        .footer {
            text-align: center;
            padding: 20px;
            color: #6c757d;
            font-size: 0.9em;
            background-color: #f8f9fa;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Todo Tasks</h1>
            <div class="subtitle">Your organized task management system</div>
        </header>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Title</th>
                        <th>Description</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>"""

            for task in tasks:
                status_class = "complete" if task.status == "Complete" else "pending"
                title_class = "completed-task" if task.status == "Complete" else ""
                html_content += f"""
                    <tr>
                        <td>{task.id}</td>
                        <td class="{title_class}">{task.title}</td>
                        <td class="{title_class}">{task.description}</td>
                        <td class="{status_class}">{task.status}</td>
                    </tr>"""

            html_content += """
                </tbody>
            </table>
        </div>
        <div class="footer">
            Generated by Todo Application | Enhanced Version
        </div>
    </div>
</body>
</html>"""

            with open("preview.html", "w", encoding="utf-8") as f:
                f.write(html_content)

            success_msg = "Tasks exported to preview.html successfully!"
            self.console.print(Panel(success_msg, title="Success", border_style="green", expand=False))
        except Exception as e:
            error_msg = f"Error exporting to HTML: {str(e)}"
            self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))

    def _dashboard(self):
        """Show a task summary dashboard panel."""
        try:
            tasks = self.task_service.list_tasks()

            # Calculate statistics
            total_tasks = len(tasks)
            completed_tasks = len([task for task in tasks if task.status == "Complete"])
            pending_tasks = len([task for task in tasks if task.status == "Pending"])

            # Create dashboard panel with statistics
            dashboard_text = Text()
            dashboard_text.append(f"[Task Dashboard]\n", style="bold blue underline")
            dashboard_text.append(f"Total Tasks: {total_tasks}\n", style="bold")
            dashboard_text.append(f"Completed: {completed_tasks}\n", style="green")
            dashboard_text.append(f"Pending: {pending_tasks}\n", style="yellow")

            if total_tasks > 0:
                completion_percentage = (completed_tasks / total_tasks) * 100
                dashboard_text.append(f"Completion: {completion_percentage:.1f}%\n",
                                    style="bold" if completion_percentage == 100 else "default")

            # Add some visual elements based on status
            if completed_tasks == total_tasks and total_tasks > 0:
                dashboard_text.append("\nAll tasks completed! Great job!", style="bold green")
            elif pending_tasks > 0 and completed_tasks > 0:
                dashboard_text.append(f"\nKeep going! {pending_tasks} tasks left to complete.", style="bold yellow")
            elif total_tasks == 0:
                dashboard_text.append("\nNo tasks yet. Add some tasks to get started!", style="italic")

            self.console.print(Panel(dashboard_text, title="Dashboard", border_style="cyan", expand=False))
        except Exception as e:
            error_msg = f"Error generating dashboard: {str(e)}"
            self.console.print(Panel(error_msg, title="Error", border_style="red", expand=False))

    def _parse_args(self, args_str: str) -> List[str]:
        """Parse command arguments, respecting quoted strings.

        Args:
            args_str: The string containing command arguments.

        Returns:
            A list of parsed arguments.
        """
        parts = []
        current_part = ""
        in_quotes = False
        quote_char = None

        i = 0
        while i < len(args_str):
            char = args_str[i]

            if char in ('"', "'") and not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
            elif char == ' ' and not in_quotes:
                if current_part:
                    parts.append(current_part)
                    current_part = ""
            else:
                current_part += char

            i += 1

        if current_part:
            parts.append(current_part)

        return parts