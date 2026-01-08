'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
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
    } finally {
      setLoading(false);
    }
  };

  const completedTasks = tasks.filter(t => t.status === 'completed').length;
  const activeTasks = tasks.filter(t => t.status !== 'completed').length;
  const completionRate = tasks.length > 0 ? (completedTasks / tasks.length) * 100 : 0;

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
          <div className="text-zinc-500 text-sm font-medium mb-1">Overview / Global</div>
          <h1 className="text-3xl font-bold text-white tracking-tight">System Status</h1>
        </div>
        <button
          onClick={() => router.push('/todo/tasks')}
          className="px-6 py-2.5 bg-white text-zinc-950 font-bold rounded-xl text-xs hover:scale-105 transition-all"
        >
          GO TO WORKSPACE
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
          {/* Main Visual Dashboard Card */}
          <div className="glass-morphism rounded-3xl overflow-hidden border border-white/5 relative group">
            <div className="absolute top-0 right-0 w-full h-full bg-linear-to-br from-primary/5 to-transparent -z-10"></div>
            <div className="p-8 pb-0">
              <div className="flex justify-between items-start mb-12">
                <div>
                  <p className="text-zinc-500 text-xs font-bold uppercase tracking-widest mb-2">Efficiency Rating</p>
                  <h2 className="text-6xl font-black text-white">{completionRate.toFixed(0)}%</h2>
                </div>
                <div className="text-right">
                  <p className="text-zinc-500 text-xs font-bold uppercase tracking-widest mb-2">Active Cycles</p>
                  <h2 className="text-3xl font-black text-white">{activeTasks}</h2>
                </div>
              </div>
            </div>

            {/* Productivity Image Mockup */}
            <div className="px-8 relative">
              <div className="absolute inset-0 bg-linear-to-t from-zinc-950 via-transparent to-transparent z-10"></div>
              <div className="relative h-[250px] w-full rounded-t-3xl overflow-hidden border-x border-t border-white/10 group-hover:border-primary/20 transition-colors">
                <img
                  src="/chart-preview.png"
                  alt="Productivity Chart"
                  className="w-full h-full object-cover opacity-60 group-hover:opacity-100 transition-opacity duration-700"
                />
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="glass-morphism rounded-3xl p-6 border border-white/5 space-y-6">
              <h3 className="text-white font-bold text-sm uppercase tracking-widest">Recent Activity</h3>
              <div className="space-y-4">
                {tasks.slice(-3).reverse().map(task => (
                  <div key={task.id} className="flex items-center space-x-4 p-3 bg-zinc-900/50 rounded-2xl border border-white/5">
                    <div className={`w-2 h-2 rounded-full ${task.status === 'completed' ? 'bg-primary' : 'bg-zinc-700'}`}></div>
                    <div className="flex-1 min-w-0">
                      <p className="text-white text-sm font-bold truncate">{task.title}</p>
                      <p className="text-zinc-500 text-[10px] uppercase">{new Date(task.updated_at).toLocaleDateString()}</p>
                    </div>
                  </div>
                ))}
                {tasks.length === 0 && <p className="text-zinc-500 text-xs italic">No recent activity found.</p>}
              </div>
            </div>

            <div className="glass-morphism rounded-3xl p-6 border border-white/5 flex flex-col justify-center items-center text-center space-y-4">
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center text-primary border border-primary/20">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0114 0z" />
                </svg>
              </div>
              <div>
                <h4 className="text-white font-bold">Focus Session</h4>
                <p className="text-zinc-500 text-xs">Ready to start your next sprint?</p>
              </div>
              <button className="w-full py-3 primary-gradient text-zinc-950 font-bold rounded-2xl text-xs emerald-glow">
                START FOCUS MODE
              </button>
            </div>
          </div>
        </div>

        <div className="space-y-8">
          <div className="glass-morphism rounded-3xl p-6 border border-white/5 bg-primary/5">
            <h3 className="text-lg font-bold text-white mb-6">Quick Entry</h3>
            <TaskForm onAddTask={async (data) => {
              if (!user?.id) return;
              const newTask = await apiClient.createTask(user.id, data);
              setTasks([...tasks, newTask]);
            }} />
          </div>

          <div className="glass-morphism rounded-3xl p-6 border border-white/5">
            <h3 className="text-white font-bold text-sm uppercase tracking-widest mb-6">Intelligence</h3>
            <div className="p-4 bg-zinc-900 border border-white/5 rounded-2xl">
              <p className="text-zinc-400 text-xs leading-relaxed italic">
                "Based on your recent patterns, you are most productive at 10:00 AM. Try scheduling your hardest tasks then."
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
