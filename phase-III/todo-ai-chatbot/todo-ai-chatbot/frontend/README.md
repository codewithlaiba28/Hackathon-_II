# Todo AI Chatbot Frontend

This is the frontend for the AI-powered Todo Chatbot that manages tasks via natural language using OpenAI Agents SDK and MCP (Model Context Protocol).

## Features

- Conversational chat interface for managing todos
- Natural language processing for task management
- Integration with backend API and MCP tools
- User authentication support

## Technology Stack

- Next.js
- React
- Better Auth for authentication
- CSS for styling

## Setup Instructions

1. Install dependencies:
```bash
npm install
```

2. Create a `.env.local` file with the following environment variables:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## Project Structure

- `pages/` - Next.js pages (including `_app.js` for global layout)
- `components/` - Reusable React components (ChatInterface.jsx)
- `contexts/` - React context providers (AuthContext.js)
- `styles/` - Global styles
- `public/` - Static assets

## API Integration

The frontend communicates with the backend API through the following endpoint:
- `POST /api/{user_id}/chat` - Send chat messages and receive AI responses

## Authentication

The application uses Better Auth for user authentication. The AuthContext provides user state management throughout the application.

## Usage

Once the application is running, you can interact with the AI chatbot by typing natural language commands such as:
- "Add a task: Buy groceries"
- "What are my tasks?"
- "Mark 'Buy groceries' as complete"
- "Delete the meeting task"
- "Update my shopping task to 'Buy milk and bread'"