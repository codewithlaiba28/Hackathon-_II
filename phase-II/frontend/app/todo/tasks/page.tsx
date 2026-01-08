'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';
import { authClient } from '@/lib/auth-client';
import TaskList from '@/components/TaskList';
import TaskForm from '@/components/TaskForm';

export default function TasksPage() {
    const [tasks, setTasks] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const router = useRouter();
    const session = authClient.useSession();
    const user = session.data?.user;

    useEffect(() => {
        if (session.isPending) return;
        if (!session.data) {
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
            if (error.message.includes('401')) router.push('/login');
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

    if (session.isPending || loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-background">
                <div className="w-12 h-12 border-4 border-primary/20 border-t-primary rounded-full animate-spin"></div>
            </div>
        );
    }

    return (
        <div className="p-4 md:p-8 space-y-8 animate-in fade-in duration-500">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <div className="text-zinc-500 text-sm font-medium mb-1">Productivity / Workspace</div>
                    <h1 className="text-3xl font-bold text-white tracking-tight">Your Tasks</h1>
                </div>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
                <div className="xl:col-span-3">
                    <TaskList
                        tasks={tasks}
                        onUpdateTask={handleUpdateTask}
                        onDeleteTask={handleDeleteTask}
                        onToggleTask={handleToggleTask}
                    />
                </div>
                <div className="xl:col-span-1">
                    <div className="glass-morphism rounded-3xl p-6 border border-white/5 sticky top-8">
                        <h3 className="text-lg font-bold text-white mb-6">Create New</h3>
                        <TaskForm onAddTask={handleAddTask} />
                    </div>
                </div>
            </div>
        </div>
    );
}
