# Tasks: Todo Application Core Features

**Feature**: Todo Application Core Features
**Branch**: 1-todo-features
**Created**: 2025-12-08
**Input**: Feature specification and implementation plan

## Implementation Strategy

Build the todo application following a layered architecture with models, services, and UI components. Implement features in priority order: Add Task (P1), View Tasks (P1), Toggle Complete (P1), Update Task (P2), Delete Task (P2). Each user story should be independently testable and deliver value.

## Dependencies

- User Story 1 (Add Task) must be completed before User Story 2 (View Tasks) can be fully tested
- Foundational components (Task model, repository, service) are prerequisites for all user stories

## Parallel Execution Examples

- Task model and repository can be developed in parallel with service layer
- CLI commands can be implemented in parallel after service layer is complete
- Each user story's CLI command can be developed independently once service is available

---

## Phase 1: Setup

**Goal**: Initialize project structure and dependencies

**Independent Test**: Project structure matches implementation plan and dependencies can be installed

- [x] T001 Create project directory structure per implementation plan: src/models/, src/services/, src/ui/, tests/
- [x] T002 Create pyproject.toml with Python 3.13+ requirement and Rich dependency
- [x] T003 Install Rich library dependency using uv

---

## Phase 2: Foundational Components

**Goal**: Build core data model and repository layer that all user stories depend on

**Independent Test**: Task can be created, stored, retrieved, updated, and deleted from in-memory repository

- [x] T004 [P] Create Task dataclass in src/models/task.py with id:int, title:str, description:str, status:str fields
- [x] T005 [P] Add validation to Task dataclass to ensure title is not empty and status is "Pending" or "Complete"
- [x] T006 [P] Create InMemoryTaskRepository in src/services/repository.py with add, get, list, update, delete, toggle methods
- [x] T007 [P] Implement auto-incrementing ID functionality in repository
- [x] T008 [P] Create TaskService in src/services/task_service.py that wraps repository operations
- [x] T009 [P] Add error handling for invalid task IDs in service methods

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1)

**Goal**: Enable users to add new tasks with a title and optional description

**Independent Test**: Can add tasks with various titles and descriptions and verify they are stored with unique IDs and pending status

- [x] T010 [US1] Implement add_task method in TaskService to create tasks with required title and optional description
- [x] T011 [US1] Set initial status to "Pending" when creating new tasks
- [x] T012 [US1] Validate that title is provided when adding tasks
- [x] T013 [US1] Create add command in CLI interface in src/ui/cli.py
- [x] T014 [US1] Parse command line arguments for add command (title and optional description)
- [x] T015 [US1] Test that add command creates tasks with unique IDs and pending status

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Enable users to view all tasks in a formatted table

**Independent Test**: Can add tasks and then view them in a table format with ID, Title, Description, and Status columns

- [x] T016 [US2] Implement list_tasks method in TaskService to return all tasks
- [x] T017 [US2] Sort tasks by ID in ascending order in list_tasks method
- [x] T018 [US2] Create list command in CLI interface in src/ui/cli.py
- [x] T019 [US2] Use Rich library to display tasks in a formatted table
- [x] T020 [US2] Include ID, Title, Description, and Status columns in the table
- [x] T021 [US2] Handle case when no tasks exist (show empty table or appropriate message)
- [x] T022 [US2] Test that list command displays all tasks in a properly formatted table

---

## Phase 5: User Story 5 - Toggle Task Completion (Priority: P1)

**Goal**: Enable users to toggle the completion status of tasks

**Independent Test**: Can toggle task completion status and verify the status changes between "Pending" and "Complete"

- [x] T023 [US5] Implement toggle_task_status method in TaskService to switch between "Pending" and "Complete"
- [x] T024 [US5] Validate that task exists before toggling status
- [x] T025 [US5] Create toggle command in CLI interface in src/ui/cli.py
- [x] T026 [US5] Parse task ID from command line arguments for toggle command
- [x] T027 [US5] Return updated task object after toggling status
- [x] T028 [US5] Test that toggle command correctly switches task status between "Pending" and "Complete"

---

## Phase 6: User Story 3 - Update Task Details (Priority: P2)

**Goal**: Enable users to update existing task details

**Independent Test**: Can update existing tasks and verify the changes are reflected

- [x] T029 [US3] Implement update_task method in TaskService to modify title and description
- [x] T030 [US3] Allow optional updates (update only title, only description, or both)
- [x] T031 [US3] Validate that task exists before updating
- [x] T032 [US3] Create update command in CLI interface in src/ui/cli.py
- [x] T033 [US3] Parse task ID, new title, and new description from command line arguments
- [x] T034 [US3] Return updated task object after modification
- [x] T035 [US3] Test that update command correctly modifies task details

---

## Phase 7: User Story 4 - Delete Tasks (Priority: P2)

**Goal**: Enable users to delete tasks by ID

**Independent Test**: Can delete tasks and verify they are removed from the system with confirmation

- [x] T036 [US4] Implement delete_task method in TaskService to remove tasks by ID
- [x] T037 [US4] Validate that task exists before deletion
- [x] T038 [US4] Return confirmation when task is deleted
- [x] T039 [US4] Create delete command in CLI interface in src/ui/cli.py
- [x] T040 [US4] Parse task ID from command line arguments for delete command
- [x] T041 [US4] Display confirmation message after successful deletion
- [x] T042 [US4] Test that delete command removes tasks and provides confirmation

---

## Phase 8: CLI Integration & REPL

**Goal**: Create complete command-line interface with REPL loop

**Independent Test**: Can run application and use all commands in continuous interaction mode

- [x] T043 Create REPL loop in src/ui/cli.py to continuously accept commands
- [x] T044 Implement command parsing for add, list, update, delete, toggle, help, exit commands
- [x] T045 Create help command that displays available commands
- [x] T046 Create exit command that terminates the application
- [x] T047 Handle invalid commands and provide helpful error messages
- [x] T048 Validate command arguments and provide appropriate feedback
- [x] T049 Test complete CLI workflow with all commands

---

## Phase 9: Main Application & Entry Point

**Goal**: Create main application entry point that initializes and runs the CLI

**Independent Test**: Can run python src/main.py and start the todo application

- [x] T050 Create main.py entry point in src/main.py
- [x] T051 Initialize TaskService with InMemoryTaskRepository
- [x] T052 Initialize CLI interface with TaskService
- [x] T053 Start REPL loop when application runs
- [x] T054 Test that application starts and CLI is accessible

---

## Phase 10: Polish & Cross-Cutting Concerns

**Goal**: Add optional features and improve user experience

**Independent Test**: Application has enhanced functionality and better user experience

- [x] T055 [P] Implement export_html command to generate preview.html for browser display
- [x] T056 [P] Create HTML template for task display with proper formatting
- [x] T057 [P] Add type hints to all functions and methods
- [x] T058 [P] Add docstrings to all classes and public methods
- [x] T059 [P] Improve error messages and user feedback
- [x] T060 [P] Add input validation for edge cases (very long titles/descriptions)
- [x] T061 [P] Write basic unit tests for core functionality
- [x] T062 [P] Create README.md with setup and usage instructions