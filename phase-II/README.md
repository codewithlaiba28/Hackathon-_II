# Todo Application

A full-stack todo application with a FastAPI backend and Next.js frontend, featuring JWT authentication and responsive design.

## Features

- **User Authentication**: Secure login/logout with JWT tokens
- **Task Management**: Create, read, update, and delete tasks
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Beautiful UI**: Clean, modern interface with Tailwind CSS
- **Security**: Each user can only access their own tasks

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLModel**: SQL database modeling and querying
- **JWT Authentication**: Secure token-based authentication
- **Python 3.8+**: Backend language

### Frontend
- **Next.js**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Better Auth**: Authentication solution

## Project Structure

```
phase-II/
├── backend/
│   ├── main.py          # Application entry point
│   ├── db.py            # Database configuration
│   ├── models.py        # Data models
│   ├── schemas.py       # Pydantic schemas
│   ├── auth.py          # Authentication logic
│   └── routers/
│       └── tasks.py     # Task-related routes
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Next.js pages
│   │   ├── lib/         # Utility functions
│   │   └── styles/      # Global styles
│   └── package.json     # Frontend dependencies
└── specs/              # Project specifications
    └── 001-ui-components/
        ├── spec.md      # Feature specification
        ├── plan.md      # Implementation plan
        └── tasks.md     # Implementation tasks
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the example:
```bash
cp .env.example .env
```

5. Update the JWT_SECRET in `.env` with a strong secret key.

6. Run the application:
```bash
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env.local` file with the API URL:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Tasks
- `GET /api/tasks` - Get all user tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task

## Security Features

- JWT tokens are required for all task-related endpoints
- Each user can only access their own tasks (enforced on the backend)
- Passwords are hashed using bcrypt
- Secure token handling with proper expiration

## Environment Variables

### Backend (.env)
- `DATABASE_URL` - Database connection string
- `JWT_SECRET` - Secret key for JWT token signing

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL` - Backend API URL

## Development

### Running in Development Mode

1. Start the backend server (port 8000)
2. Start the frontend server (port 3000)
3. Access the application at `http://localhost:3000`

### API Testing

You can test the API endpoints using tools like Postman or curl:

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Get tasks (with JWT token)
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

## Deployment

### Backend
- Deploy the FastAPI application to a server or cloud platform
- Configure environment variables
- Set up a production database

### Frontend
- Build the Next.js application: `npm run build`
- Deploy the build output to a static hosting service
- Configure environment variables for the deployed API URL

## License

This project is licensed under the MIT License.