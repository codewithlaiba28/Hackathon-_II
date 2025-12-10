from src.services.repository import InMemoryTaskRepository
from src.services.task_service import TaskService
from src.ui.cli import TodoCLI


def main():
    """Main entry point for the todo application."""
    # Initialize the repository
    repository = InMemoryTaskRepository()

    # Initialize the task service with the repository
    task_service = TaskService(repository)

    # Initialize the CLI with the task service
    cli = TodoCLI(task_service)

    # Start the REPL loop
    cli.run()


if __name__ == "__main__":
    main()