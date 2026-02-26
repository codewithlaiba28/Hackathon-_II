# Quickstart: UI Components

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Git for version control

## Setup Instructions

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   # or
   yarn install
   ```

2. **Environment Configuration**
   ```bash
   # Copy environment template
   cp .env.example .env.local
   # Update environment variables as needed
   ```

3. **Run Development Server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. **Access the Application**
   - Landing Page: http://localhost:3000
   - Todo Dashboard: http://localhost:3000/todo

## Key Components

### Landing Page Components
- `Navbar`: Responsive navigation bar
- `HeroSection`: Eye-catching hero section with "Go to Todo" button
- `AboutSection`: Brief introduction about the todo app
- `Footer`: Professional footer with links

### Todo App Components
- `TaskList`: Displays tasks in responsive cards
- `TaskItem`: Individual task representation
- `TaskForm`: Form for creating/editing tasks
- `TaskDashboard`: Main dashboard layout
- `AuthButton`: Authentication integration component

## API Integration
Components fetch data via `/lib/api.ts` and automatically attach JWT tokens from Better Auth for authenticated requests.

## Styling
All components use Tailwind CSS utility classes for consistent, responsive design that works across mobile, tablet, and desktop devices.