---
name: frontend-component-testing
description: |
  This skill creates comprehensive tests for React/Next.js components including unit tests, integration tests, and UI interaction testing. Use this skill when you need to implement thorough testing for your frontend components.
---

# Frontend Component Testing Skill

This skill should be used when users need to create comprehensive tests for React/Next.js components including unit tests, integration tests, and UI interaction testing.

## Skill Type: Automation

## Domain: Frontend Component Testing with React/Next.js

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing components, testing setup, UI patterns, and state management |
| **Conversation** | User's specific testing requirements, coverage needs, and CI/CD constraints |
| **Skill References** | React testing library documentation, Jest best practices, UI testing patterns |
| **User Guidelines** | Project-specific testing conventions, coverage thresholds, accessibility requirements |

Ensure all required context is gathered before implementing.

## Core Concepts

Frontend component testing involves:
- Unit testing of individual components
- Integration testing of component interactions
- UI interaction testing with user events
- State management testing
- Accessibility testing
- Performance testing considerations

## Testing Workflow

The component testing process follows these steps:
1. Set up testing environment with Jest and React Testing Library
2. Create test utilities and helpers
3. Write unit tests for individual components
4. Write integration tests for component interactions
5. Test user interactions and state changes
6. Run tests and analyze results

## Implementation Steps

### 1. Setup Testing Environment

First, install the necessary testing dependencies:

```bash
# Install testing libraries
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event jest jest-environment-jsdom
```

Create the Jest configuration file:

```javascript
// frontend/jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  testPathIgnorePatterns: ['/node_modules/', '/.next/'],
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/node_modules/**',
  ],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
};
```

Create the Jest setup file:

```javascript
// frontend/jest.setup.js
import '@testing-library/jest-dom';

// Mock Next.js features
jest.mock('next/router', () => require('next-router-mock'));
```

### 2. Create Test Utilities

Create utilities for testing components:

```typescript
// frontend/test-utils.tsx
import React, { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { AuthProvider } from '@/components/session-provider';

// Create a custom render function with providers
const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) => render(ui, { wrapper: AuthProvider, ...options });

// Re-export everything
export * from '@testing-library/react';

// Override render method
export { customRender as render };
```

### 3. Write Unit Tests for Components

Create unit tests for individual components:

```typescript
// frontend/__tests__/TaskItem.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@/test-utils';
import { TaskItem } from '@/components/TaskItem';
import { Task } from '@/types/task';

describe('TaskItem Component', () => {
  const mockTask: Task = {
    id: '1',
    title: 'Test Task',
    description: 'Test Description',
    status: 'pending',
    priority: 'medium',
    user_id: 'user1',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };

  const mockOnUpdate = jest.fn();
  const mockOnDelete = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders task title and description', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
  });

  it('displays correct status badge', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    expect(screen.getByText('pending')).toBeInTheDocument();
  });

  it('displays correct priority badge', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    expect(screen.getByText('medium')).toBeInTheDocument();
  });

  it('calls onUpdate when status is toggled', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    const statusToggle = screen.getByRole('button', { name: /toggle status/i });
    fireEvent.click(statusToggle);

    expect(mockOnUpdate).toHaveBeenCalledWith({
      ...mockTask,
      status: 'completed'
    });
  });

  it('calls onDelete when delete button is clicked', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    const deleteButton = screen.getByRole('button', { name: /delete/i });
    fireEvent.click(deleteButton);

    expect(mockOnDelete).toHaveBeenCalledWith(mockTask.id);
  });

  it('renders edit button when task is not completed', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    expect(screen.getByRole('button', { name: /edit/i })).toBeInTheDocument();
  });

  it('does not render edit button when task is completed', () => {
    const completedTask = { ...mockTask, status: 'completed' };

    render(
      <TaskItem
        task={completedTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    expect(screen.queryByRole('button', { name: /edit/i })).not.toBeInTheDocument();
  });
});
```

### 4. Write Integration Tests

Create integration tests for component interactions:

```typescript
// frontend/__tests__/TaskList.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@/test-utils';
import { TaskList } from '@/components/TaskList';
import { Task } from '@/types/task';

describe('TaskList Component', () => {
  const mockTasks: Task[] = [
    {
      id: '1',
      title: 'Task 1',
      description: 'First task',
      status: 'pending',
      priority: 'high',
      user_id: 'user1',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      id: '2',
      title: 'Task 2',
      description: 'Second task',
      status: 'completed',
      priority: 'medium',
      user_id: 'user1',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
  ];

  const mockOnUpdate = jest.fn();
  const mockOnDelete = jest.fn();
  const mockOnCreate = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders all tasks', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
        onCreate={mockOnCreate}
      />
    );

    expect(screen.getByText('Task 1')).toBeInTheDocument();
    expect(screen.getByText('Task 2')).toBeInTheDocument();
  });

  it('filters tasks by status', async () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
        onCreate={mockOnCreate}
      />
    );

    // Initially show all tasks
    expect(screen.getByText('Task 1')).toBeInTheDocument();
    expect(screen.getByText('Task 2')).toBeInTheDocument();

    // Filter by completed
    const completedFilter = screen.getByRole('button', { name: /completed/i });
    fireEvent.click(completedFilter);

    await waitFor(() => {
      expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
      expect(screen.getByText('Task 2')).toBeInTheDocument();
    });
  });

  it('filters tasks by priority', async () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
        onCreate={mockOnCreate}
      />
    );

    // Filter by high priority
    const highPriorityFilter = screen.getByRole('button', { name: /high/i });
    fireEvent.click(highPriorityFilter);

    await waitFor(() => {
      expect(screen.getByText('Task 1')).toBeInTheDocument();
      expect(screen.queryByText('Task 2')).not.toBeInTheDocument();
    });
  });

  it('calls onUpdate when a task is updated', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
        onCreate={mockOnCreate}
      />
    );

    const statusToggle = screen.getAllByRole('button', { name: /toggle status/i })[0];
    fireEvent.click(statusToggle);

    expect(mockOnUpdate).toHaveBeenCalledWith({
      ...mockTasks[0],
      status: 'completed'
    });
  });

  it('calls onDelete when a task is deleted', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
        onCreate={mockOnCreate}
      />
    );

    const deleteButtons = screen.getAllByRole('button', { name: /delete/i });
    fireEvent.click(deleteButtons[0]);

    expect(mockOnDelete).toHaveBeenCalledWith('1');
  });
});
```

### 5. Write Form Component Tests

Create tests for form components:

```typescript
// frontend/__tests__/TaskForm.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@/test-utils';
import { TaskForm } from '@/components/TaskForm';

describe('TaskForm Component', () => {
  const mockOnSubmit = jest.fn();
  const mockOnCancel = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders form fields', () => {
    render(
      <TaskForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
        initialTask={null}
      />
    );

    expect(screen.getByLabelText(/title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/status/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/priority/i)).toBeInTheDocument();
  });

  it('submits form with valid data', async () => {
    render(
      <TaskForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
        initialTask={null}
      />
    );

    fireEvent.change(screen.getByLabelText(/title/i), {
      target: { value: 'New Task' }
    });
    fireEvent.change(screen.getByLabelText(/description/i), {
      target: { value: 'New Task Description' }
    });
    fireEvent.change(screen.getByLabelText(/status/i), {
      target: { value: 'pending' }
    });
    fireEvent.change(screen.getByLabelText(/priority/i), {
      target: { value: 'high' }
    });

    fireEvent.click(screen.getByRole('button', { name: /save/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        title: 'New Task',
        description: 'New Task Description',
        status: 'pending',
        priority: 'high'
      });
    });
  });

  it('shows validation errors for empty title', async () => {
    render(
      <TaskForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
        initialTask={null}
      />
    );

    fireEvent.click(screen.getByRole('button', { name: /save/i }));

    await waitFor(() => {
      expect(screen.getByText(/title is required/i)).toBeInTheDocument();
    });
  });

  it('populates form with initial task data', () => {
    const initialTask = {
      id: '1',
      title: 'Existing Task',
      description: 'Existing Description',
      status: 'completed',
      priority: 'low',
      user_id: 'user1',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    render(
      <TaskForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
        initialTask={initialTask}
      />
    );

    expect(screen.getByDisplayValue('Existing Task')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Existing Description')).toBeInTheDocument();
    expect(screen.getByRole('combobox', { value: 'completed' })).toBeInTheDocument();
    expect(screen.getByRole('combobox', { value: 'low' })).toBeInTheDocument();
  });

  it('calls onCancel when cancel button is clicked', () => {
    render(
      <TaskForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
        initialTask={null}
      />
    );

    fireEvent.click(screen.getByRole('button', { name: /cancel/i }));

    expect(mockOnCancel).toHaveBeenCalled();
  });
});
```

### 6. Write API Integration Tests

Create tests that verify API interactions:

```typescript
// frontend/__tests__/api-integration.test.tsx
import React from 'react';
import { render, screen, waitFor, fireEvent } from '@/test-utils';
import { TaskList } from '@/components/TaskList';
import { apiClient } from '@/lib/api-client';
import { Task } from '@/types/task';

// Mock the API client
jest.mock('@/lib/api-client', () => ({
  apiClient: {
    getTasks: jest.fn(),
    createTask: jest.fn(),
    updateTask: jest.fn(),
    deleteTask: jest.fn(),
  },
}));

describe('API Integration Tests', () => {
  const mockTasks: Task[] = [
    {
      id: '1',
      title: 'API Test Task',
      description: 'Task from API',
      status: 'pending',
      priority: 'medium',
      user_id: 'user1',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
  ];

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('fetches and displays tasks from API', async () => {
    (apiClient.getTasks as jest.MockedFunction<any>).mockResolvedValue(mockTasks);

    render(<TaskList tasks={mockTasks} onUpdate={jest.fn()} onDelete={jest.fn()} onCreate={jest.fn()} />);

    await waitFor(() => {
      expect(screen.getByText('API Test Task')).toBeInTheDocument();
    });

    expect(apiClient.getTasks).toHaveBeenCalled();
  });

  it('creates a new task via API', async () => {
    (apiClient.createTask as jest.MockedFunction<any>).mockResolvedValue({
      id: '2',
      title: 'New Task',
      description: 'New Description',
      status: 'pending',
      priority: 'high',
      user_id: 'user1',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });

    const { getByLabelText, getByRole } = render(
      <TaskForm onSubmit={jest.fn()} onCancel={jest.fn()} initialTask={null} />
    );

    fireEvent.change(getByLabelText(/title/i), { target: { value: 'New Task' } });
    fireEvent.change(getByLabelText(/description/i), { target: { value: 'New Description' } });
    fireEvent.click(getByRole('button', { name: /save/i }));

    await waitFor(() => {
      expect(apiClient.createTask).toHaveBeenCalledWith({
        title: 'New Task',
        description: 'New Description',
        status: 'pending',
        priority: 'high'
      });
    });
  });

  it('updates a task via API', async () => {
    const updatedTask = { ...mockTasks[0], status: 'completed' };
    (apiClient.updateTask as jest.MockedFunction<any>).mockResolvedValue(updatedTask);

    render(<TaskList tasks={mockTasks} onUpdate={jest.fn()} onDelete={jest.fn()} onCreate={jest.fn()} />);

    const statusToggle = screen.getByRole('button', { name: /toggle status/i });
    fireEvent.click(statusToggle);

    await waitFor(() => {
      expect(apiClient.updateTask).toHaveBeenCalledWith('1', {
        status: 'completed'
      });
    });
  });

  it('deletes a task via API', async () => {
    (apiClient.deleteTask as jest.MockedFunction<any>).mockResolvedValue({ success: true });

    render(<TaskList tasks={mockTasks} onUpdate={jest.fn()} onDelete={jest.fn()} onCreate={jest.fn()} />);

    const deleteButton = screen.getByRole('button', { name: /delete/i });
    fireEvent.click(deleteButton);

    await waitFor(() => {
      expect(apiClient.deleteTask).toHaveBeenCalledWith('1');
    });
  });
});
```

### 7. Write Accessibility Tests

Create tests to ensure accessibility:

```typescript
// frontend/__tests__/accessibility.test.tsx
import React from 'react';
import { render, screen } from '@/test-utils';
import { TaskItem } from '@/components/TaskItem';
import { TaskForm } from '@/components/TaskForm';
import { Task } from '@/types/task';

describe('Accessibility Tests', () => {
  const mockTask: Task = {
    id: '1',
    title: 'Accessible Task',
    description: 'Task description',
    status: 'pending',
    priority: 'medium',
    user_id: 'user1',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };

  it('TaskItem has proper ARIA attributes', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={jest.fn()}
        onDelete={jest.fn()}
      />
    );

    const taskItem = screen.getByRole('listitem');
    expect(taskItem).toBeInTheDocument();

    // Check that buttons have proper labels
    expect(screen.getByRole('button', { name: /toggle status/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /edit/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /delete/i })).toBeInTheDocument();
  });

  it('TaskForm has proper form labels', () => {
    render(
      <TaskForm
        onSubmit={jest.fn()}
        onCancel={jest.fn()}
        initialTask={null}
      />
    );

    // Check that all form fields have associated labels
    expect(screen.getByLabelText(/title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/status/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/priority/i)).toBeInTheDocument();

    // Check that buttons have proper names
    expect(screen.getByRole('button', { name: /save/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /cancel/i })).toBeInTheDocument();
  });

  it('TaskList has proper semantic structure', () => {
    render(
      <TaskList
        tasks={[mockTask]}
        onUpdate={jest.fn()}
        onDelete={jest.fn()}
        onCreate={jest.fn()}
      />
    );

    // Check for proper list structure
    const list = screen.getByRole('list');
    expect(list).toBeInTheDocument();

    const listItems = screen.getAllByRole('listitem');
    expect(listItems).toHaveLength(1);
  });
});
```

### 8. Create Test Configuration

Set up comprehensive test configuration:

```json
// frontend/package.json (add to scripts)
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:ui": "npm run test -- --watch"
  }
}
```

Create a test helper for complex scenarios:

```typescript
// frontend/test-helpers.ts
import { render } from '@/test-utils';
import { Task } from '@/types/task';

// Helper to create a task with default values
export const createMockTask = (overrides: Partial<Task> = {}): Task => ({
  id: overrides.id || '1',
  title: overrides.title || 'Test Task',
  description: overrides.description || 'Test Description',
  status: overrides.status || 'pending',
  priority: overrides.priority || 'medium',
  user_id: overrides.user_id || 'user1',
  created_at: overrides.created_at || new Date().toISOString(),
  updated_at: overrides.updated_at || new Date().toISOString(),
});

// Helper to render components with common providers
export const renderWithProviders = (component: React.ReactElement) => {
  return render(component);
};

// Helper for async testing
export const waitForElement = async (queryFn: () => HTMLElement | null) => {
  return new Promise<HTMLElement>((resolve) => {
    const interval = setInterval(() => {
      const element = queryFn();
      if (element) {
        clearInterval(interval);
        resolve(element);
      }
    }, 10);
  });
};
```

## Best Practices

1. **Use React Testing Library** for component testing
2. **Test user interactions** rather than implementation details
3. **Use meaningful test names** that describe the behavior
4. **Test both positive and negative cases**
5. **Mock external dependencies** like API calls
6. **Test accessibility** features
7. **Use proper selectors** (byRole, byLabelText, etc.)
8. **Write focused tests** that test one thing at a time

## Test Coverage Checklist

- [ ] Unit tests for all components
- [ ] Integration tests for component interactions
- [ ] Form validation tests
- [ ] API integration tests
- [ ] Accessibility tests
- [ ] Error handling tests
- [ ] Loading state tests
- [ ] Empty state tests
- [ ] User interaction tests
- [ ] Responsive design tests

## Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run specific test file
npm test TaskItem.test.tsx
```

This skill provides a comprehensive approach to frontend component testing for React/Next.js applications, ensuring thorough testing of UI components, user interactions, and API integrations.