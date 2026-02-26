# Enhanced Todo Application

A command-line in-memory todo application built with Python and Rich for beautiful formatting. Features an enhanced UI with professional styling and hackathon-ready design.

## Features

- Add new tasks with title and optional description
- View all tasks in a formatted table with rounded borders and alternating row styles
- Update existing task details
- Delete tasks by ID
- Toggle task completion status (with strikethrough for completed tasks)
- Export tasks to professional HTML preview
- Enhanced UI with panels, colors, and professional styling

## Requirements

- Python 3.13+
- Rich library

## Installation

1. Clone the repository
2. Install dependencies using uv:
   ```bash
   uv sync
   ```
   or using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python src/main.py
```

The application will start in REPL mode where you can use the following commands:

- `add <title> [description]` - Add a new task
- `list` - List all tasks in a formatted table
- `show` - Show all tasks (alias for list)
- `update <id> [new_title] [new_description]` - Update a task
- `update tasks <id> [new_title] [new_description]` - Update a task (alternative format)
- `delete <id>` - Delete a task
- `toggle <id>` - Toggle task completion status
- `dashboard` - Show task summary dashboard
- `export_html` - Export tasks to HTML for browser preview
- `help` - Show available commands
- `exit` - Exit the application

## Example Workflow

```
todo> add "Buy groceries" "Milk, bread, eggs"
[Success panel with task details]

todo> add "Walk the dog"
[Success panel with task details]

todo> list
[Shows a formatted table with your tasks using rounded borders and alternating row styles]

todo> toggle 1
[Success panel showing status change]

todo> export_html
[Generates preview.html with professional HTML styling]

todo> exit
[Goodbye panel]
```

## Enhanced UI Features

### Terminal UI
- **Rounded borders** and **alternating row styles** in task tables
- **Strikethrough text** for completed tasks
- **Color-coded status** (yellow for Pending, green for Complete)
- **Panels** for welcome message, commands, and success/error messages
- **Professional styling** with Rich formatting

### Browser Preview
- **Professional HTML export** with modern CSS styling
- **Responsive design** with gradient headers
- **Color-coded status** and **strikethrough for completed tasks**
- **Hover effects** and **modern UI elements**

## Architecture

The application follows a layered architecture:

- **Models**: Task dataclass with validation
- **Services**: Business logic layer (TaskService)
- **Repository**: Data access layer (InMemoryTaskRepository)
- **UI**: Enhanced command-line interface with Rich formatting

## How to Run and Preview HTML

1. **Start the application:**
   ```bash
   python src/main.py
   ```

2. **Add some tasks and use the app:**
   ```
   todo> add "Sample Task" "This is a sample task description"
   todo> list
   todo> toggle 1
   ```

3. **Export to HTML:**
   ```
   todo> export_html
   ```

4. **Open the HTML preview:**
   - Open `preview.html` in your web browser to see the professional HTML version

## Hackathon Demo Commands

For a quick demo, try this sequence:
```
todo> add "Prepare presentation" "Create slides for the demo"
todo> add "Practice speech" "Rehearse the presentation"
todo> add "Gather feedback" "Collect feedback from team"
todo> list
todo> toggle 1
todo> list
todo> export_html
```

## License

MIT