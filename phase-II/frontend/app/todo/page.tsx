'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/lib/api';
import { authClient } from '@/lib/auth-client';
import TaskList from '@/components/TaskList';
import TaskForm from '@/components/TaskForm';

export default function TodoPage() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const checkAuthAndFetchTasks = async () => {
      try {
        // Check for JWT token in localStorage (primary auth check)
        const jwtToken = localStorage.getItem('jwt_token');

        if (!jwtToken) {
          console.log('No JWT token found, redirecting to login');
          router.push('/login');
          return;
        }

        // JWT token exists, check Better Auth session (optional, for frontend state)
        const { data } = await authClient.getSession();
        if (data?.session) {
          console.log('✅ Both JWT token and Better Auth session present');
        } else {
          console.log('⚠️ JWT token present, Better Auth session missing - continuing with JWT');
        }

        // Fetch tasks using JWT token
        fetchTasks();
        setLoading(false);
      } catch (error) {
        console.error('Auth check or fetch tasks failed', error);
        router.push('/login');
      }
    };

    checkAuthAndFetchTasks();
  }, [router]);

  const fetchTasks = async () => {
    try {
      const data = await apiClient.get('/api/tasks/');
      setTasks(data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      // If unauthorized, redirect to login
      if (error instanceof Error &&
        (error.message.includes('401') ||
          error.message.includes('403') ||
          error.message.includes('Could not validate credentials'))) {
        router.push('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (taskData: { title: string; description?: string }) => {
    try {
      const newTask = await apiClient.post('/api/tasks/', taskData);
      setTasks([...tasks, newTask]);
    } catch (error) {
      console.error('Error adding task:', error);
      // If unauthorized, redirect to login
      if (error instanceof Error && error.message.includes('401')) {
        router.push('/login');
      }
    }
  };

  const handleUpdateTask = async (id: string, taskData: { title?: string; description?: string; status?: string }) => {
    try {
      const updatedTask = await apiClient.put(`/api/tasks/${id}`, taskData);
      setTasks(tasks.map(task => task.id === id ? updatedTask : task));
    } catch (error) {
      console.error('Error updating task:', error);
      // If unauthorized, redirect to login
      if (error instanceof Error && error.message.includes('401')) {
        router.push('/login');
      }
    }
  };

  const handleDeleteTask = async (id: string) => {
    try {
      await apiClient.delete(`/api/tasks/${id}`);
      setTasks(tasks.filter(task => task.id !== id));
    } catch (error) {
      console.error('Error deleting task:', error);
      // If unauthorized, redirect to login
      if (error instanceof Error && error.message.includes('401')) {
        router.push('/login');
      }
    }
  };

  const handleToggleTask = async (id: string) => {
    try {
      const task = tasks.find(t => t.id === id);
      if (task) {
        const updatedTask = await apiClient.put(`/api/tasks/${id}`, {
          status: task.status === 'pending' ? 'completed' : 'pending'
        });
        setTasks(tasks.map(task => task.id === id ? updatedTask : task));
      }
    } catch (error) {
      console.error('Error toggling task:', error);
      // If unauthorized, redirect to login
      if (error instanceof Error && error.message.includes('401')) {
        router.push('/login');
      }
    }
  };

  const handleLogout = async () => {
    try {
      await authClient.signOut();
      router.push('/login');
    } catch (error) {
      console.error('Logout error:', error);
      // Better Auth handles cleanup automatically
      router.push('/login');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-2xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-red-950 py-8 relative">
      {/* Abstract Background Shapes */}
      <div className="fixed inset-0 overflow-hidden -z-10">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-red-600 rounded-full mix-blend-screen filter blur-3xl opacity-20 animate-blob"></div>
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-red-800 rounded-full mix-blend-screen filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute bottom-0 left-1/2 w-96 h-96 bg-gray-800 rounded-full mix-blend-screen filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="flex justify-between items-center mb-8">
          <div className="flex flex-col">
            <Link href="/" className="text-gray-400 hover:text-white mb-2 inline-flex items-center transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              Back to Home
            </Link>
            <h1 className="text-3xl font-bold text-white">Todo App</h1>
          </div>
          <button
            onClick={handleLogout}
            className="bg-red-600 hover:bg-red-800 text-white font-bold py-2 px-4 rounded transition-colors"
          >
            Logout
          </button>
        </div>

        <TaskForm onAddTask={handleAddTask} />
        <TaskList
          tasks={tasks}
          onUpdateTask={handleUpdateTask}
          onDeleteTask={handleDeleteTask}
          onToggleTask={handleToggleTask}
        />
      </div>
    </div>
  );
}