# Data Model: UI Components

## Task Entity
- **title**: string - The task title/description
- **description**: string (optional) - Detailed description of the task
- **status**: string - Task status (e.g., "pending", "completed", "in-progress")
- **createdAt**: Date - Timestamp when task was created
- **updatedAt**: Date - Timestamp when task was last updated
- **userId**: string - ID of the user who owns the task (for security verification)

## User Entity
- **id**: string - Unique user identifier
- **email**: string - User's email address
- **name**: string (optional) - User's display name
- **createdAt**: Date - Account creation timestamp
- **lastLoginAt**: Date (optional) - Last login timestamp

## Page Entity
- **route**: string - The page route (e.g., "/", "/todo")
- **title**: string - Page title for SEO and accessibility
- **layout**: string - Layout structure for the page
- **requiresAuth**: boolean - Whether the page requires authentication

## Component State Models

### TaskForm State
- **title**: string - Current input value for task title
- **description**: string - Current input value for task description
- **isSubmitting**: boolean - Whether the form is currently submitting
- **errors**: object - Validation errors for form fields

### TaskList State
- **tasks**: array - List of tasks to display
- **isLoading**: boolean - Whether tasks are being loaded
- **error**: string (optional) - Error message if loading failed
- **filter**: string - Current filter (e.g., "all", "completed", "pending")

### AuthButton State
- **isAuthenticated**: boolean - Current authentication status
- **isLoading**: boolean - Whether auth status is being checked
- **user**: object (optional) - User data when authenticated