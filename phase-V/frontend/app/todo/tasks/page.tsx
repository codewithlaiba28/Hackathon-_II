'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';
import { authClient } from '@/lib/auth-client';
import TaskList from '@/components/TaskList';
import TaskForm from '@/components/TaskForm';
import { useToast } from '@/components/ui/use-toast';

export default function TasksPage() {
    const [tasks, setTasks] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isFirstLoad, setIsFirstLoad] = useState(true);
    const [search, setSearch] = useState('');
    const [priorityFilter, setPriorityFilter] = useState('');
    const [statusFilter, setStatusFilter] = useState('');
    const [sortBy, setSortBy] = useState('created_at');
    const [sortOrder, setSortOrder] = useState('desc');
    const [tagFilter, setTagFilter] = useState('');

    const router = useRouter();
    const session = authClient.useSession();
    const user = session.data?.user;
    const { toast } = useToast();

    // Initial load — show spinner only the first time
    useEffect(() => {
        if (session.isPending) return;
        if (!session.data) {
            router.push('/login');
            return;
        }
        if (isFirstLoad) {
            fetchTasks(true);
            setIsFirstLoad(false);
        }

        // Listen for updates from chatbot or events
        const handleUpdate = () => {
            console.log("Refreshing tasks due to update...");
            fetchTasks(false);
        };

        window.addEventListener('tasks-updated', handleUpdate);
        return () => window.removeEventListener('tasks-updated', handleUpdate);
    }, [session.isPending, session.data, router]);

    // Refetch silently when filters/sort change (no spinner)
    useEffect(() => {
        if (!isFirstLoad && user?.id) {
            fetchTasks(false);
        }
    }, [search, priorityFilter, statusFilter, tagFilter, sortBy, sortOrder]);

    const fetchTasks = async (showSpinner = false) => {
        if (!user?.id) return;
        try {
            if (showSpinner) setIsLoading(true);
            const params = {
                search,
                priority: priorityFilter,
                status: statusFilter,
                tag: tagFilter,
                sort_by: sortBy,
                order: sortOrder
            };

            // Clean undefined/empty params
            const cleanParams = Object.keys(params).reduce((acc: any, key) => {
                if (params[key as keyof typeof params]) {
                    acc[key] = params[key as keyof typeof params];
                }
                return acc;
            }, {});

            const data = await apiClient.getTasks(user.id, cleanParams);
            setTasks(data);
        } catch (error: any) {
            console.error('Error fetching tasks:', error);
            if (error.message && error.message.includes('401')) router.push('/login');
        } finally {
            setIsLoading(false);
        }
    };

    const handleAddTask = async (taskData: any) => {
        if (!user?.id) return;
        try {
            const newTask = await apiClient.createTask(user.id, taskData);
            setTasks([newTask, ...tasks]);
            toast({
                title: "Success",
                description: "Task created successfully",
            });
            fetchTasks(); // Refresh to ensure correct sort order
        } catch (error: any) {
            console.error('Error adding task:', error);
            toast({
                title: "Error",
                description: "Failed to create task",
                variant: "destructive"
            });
        }
    };

    const handleUpdateTask = async (id: string, taskData: { title?: string; description?: string; status?: string }) => {
        if (!user?.id) return;
        try {
            const updatedTask = await apiClient.updateTask(user.id, id, taskData);
            setTasks(tasks.map(task => task.id === id ? updatedTask : task));
            toast({
                title: "Success",
                description: "Task updated successfully",
            });
        } catch (error: any) {
            console.error('Error updating task:', error);
            toast({
                title: "Error",
                description: "Failed to update task",
                variant: "destructive"
            });
        }
    };

    const handleDeleteTask = async (id: string) => {
        if (!user?.id) return;
        try {
            await apiClient.deleteTask(user.id, id);
            setTasks(tasks.filter(task => task.id !== id));
            toast({
                title: "Success",
                description: "Task deleted successfully",
            });
        } catch (error: any) {
            console.error('Error deleting task:', error);
            toast({
                title: "Error",
                description: "Failed to delete task",
                variant: "destructive"
            });
        }
    };

    const handleToggleTask = async (id: string) => {
        if (!user?.id) return;
        try {
            // Note: apiClient might have toggleTask or toggleTaskComplete depending on version
            // Assuming toggleTask based on previous read, but checking api.ts would be safer.
            // In step 177 read, it was `toggleTask`.
            const updatedTask = await apiClient.toggleTask(user.id, id);
            setTasks(tasks.map(task => task.id === id ? updatedTask : task));
        } catch (error: any) {
            console.error('Error toggling task:', error);
            toast({
                title: "Error",
                description: "Failed to update task status",
                variant: "destructive"
            });
        }
    };

    if (session.isPending) {
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
                    <h1 className="text-3xl font-bold text-white tracking-tight">My Tasks</h1>
                    <p className="text-zinc-400 mt-1">Manage and organize your daily work</p>
                </div>
                <div className="flex bg-zinc-900/50 p-1 rounded-xl border border-white/5">
                    <button className="px-4 py-2 bg-primary/10 text-primary rounded-lg text-sm font-medium transition-all">
                        List View
                    </button>
                    <button className="px-4 py-2 text-zinc-400 hover:text-white rounded-lg text-sm font-medium transition-all">
                        Board View
                    </button>
                </div>
            </div>

            {/* Filters and Search */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 p-4 glass-morphism rounded-2xl border border-white/5">
                <div className="col-span-1 md:col-span-1">
                    <input
                        type="text"
                        placeholder="Search tasks..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        className="w-full px-4 py-2 bg-zinc-900 border border-white/10 rounded-xl text-white focus:outline-none focus:border-primary text-sm"
                    />
                </div>
                <div className="flex flex-wrap gap-2 col-span-1 md:col-span-3 items-center">
                    <select
                        value={priorityFilter}
                        onChange={(e) => setPriorityFilter(e.target.value)}
                        className="px-3 py-2 bg-zinc-900 border border-white/10 rounded-xl text-white text-sm focus:outline-none"
                    >
                        <option value="">All Priorities</option>
                        <option value="high">High</option>
                        <option value="medium">Medium</option>
                        <option value="low">Low</option>
                    </select>
                    <select
                        value={statusFilter}
                        onChange={(e) => setStatusFilter(e.target.value)}
                        className="px-3 py-2 bg-zinc-900 border border-white/10 rounded-xl text-white text-sm focus:outline-none"
                    >
                        <option value="">All Statuses</option>
                        <option value="pending">Pending</option>
                        <option value="completed">Completed</option>
                    </select>
                    <select
                        value={sortBy}
                        onChange={(e) => setSortBy(e.target.value)}
                        className="px-3 py-2 bg-zinc-900 border border-white/10 rounded-xl text-white text-sm focus:outline-none"
                    >
                        <option value="created_at">Date Created</option>
                        <option value="due_date">Due Date</option>
                        <option value="priority">Priority</option>
                    </select>
                    <button
                        onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                        className="px-3 py-2 bg-zinc-900 border border-white/10 rounded-xl text-white text-sm hover:bg-zinc-800 transition-colors"
                        title={sortOrder === 'asc' ? 'Ascending' : 'Descending'}
                    >
                        {sortOrder === 'asc' ? '↑' : '↓'}
                    </button>
                    {tagFilter && (
                        <button
                            onClick={() => setTagFilter('')}
                            className="px-3 py-2 bg-red-500/10 text-red-500 border border-red-500/20 rounded-xl text-sm hover:bg-red-500/20 transition-colors"
                        >
                            Clear Tag: {tagFilter}
                        </button>
                    )}
                </div>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
                <div className="xl:col-span-2">
                    {isLoading ? (
                        <div className="flex justify-center py-12">
                            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary"></div>
                        </div>
                    ) : (
                        <TaskList
                            tasks={tasks}
                            onUpdateTask={handleUpdateTask}
                            onDeleteTask={handleDeleteTask}
                            onToggleTask={handleToggleTask}
                        />
                    )}
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
