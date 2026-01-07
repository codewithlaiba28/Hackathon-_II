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
  const session = authClient.useSession();
  const user = session.data?.user;

  useEffect(() => {
    if (session.isPending) return;

    if (!session.data) {
      console.log('No session found, redirecting to login');
      router.push('/login');
      return;
    }

    fetchTasks();
  }, [session.isPending, session.data, router]);

  const fetchTasks = async () => {
    if (!user?.id) return;
    try {
      const data = await apiClient.getTasks(user.id);
      setTasks(data);
    } catch (error: any) {
      console.error('Error fetching tasks:', error);
      if (error.message.includes('401') || error.message.includes('Unauthorized')) {
        router.push('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (taskData: { title: string; description?: string }) => {
    if (!user?.id) return;
    try {
      const newTask = await apiClient.createTask(user.id, taskData);
      setTasks([...tasks, newTask]);
    } catch (error: any) {
      console.error('Error adding task:', error);
    }
  };

  const handleUpdateTask = async (id: string, taskData: { title?: string; description?: string; status?: string }) => {
    if (!user?.id) return;
    try {
      const updatedTask = await apiClient.updateTask(user.id, id, taskData);
      setTasks(tasks.map(task => task.id === id ? updatedTask : task));
    } catch (error: any) {
      console.error('Error updating task:', error);
    }
  };

  const handleDeleteTask = async (id: string) => {
    if (!user?.id) return;
    try {
      await apiClient.deleteTask(user.id, id);
      setTasks(tasks.filter(task => task.id !== id));
    } catch (error: any) {
      console.error('Error deleting task:', error);
    }
  };

  const handleToggleTask = async (id: string) => {
    if (!user?.id) return;
    try {
      const updatedTask = await apiClient.toggleTask(user.id, id);
      setTasks(tasks.map(task => task.id === id ? updatedTask : task));
    } catch (error: any) {
      console.error('Error toggling task:', error);
    }
  };

  const handleLogout = async () => {
    try {
      await authClient.signOut();
      localStorage.clear(); // Clear any remaining legacy items
      router.push('/login');
    } catch (error) {
      console.error('Logout error:', error);
      router.push('/login');
    }
  };

  if (session.isPending || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-2xl text-white">Loading...</div>
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
            {user && <p className="text-gray-400 text-sm mt-1">Logged in as {user.email}</p>}
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
