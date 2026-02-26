import { useState } from 'react';

interface TaskFormProps {
  onAddTask: (taskData: { title: string; description?: string }) => void;
}

export default function TaskForm({ onAddTask }: TaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (title.trim()) {
      onAddTask({ title: title.trim(), description: description.trim() || undefined });
      setTitle('');
      setDescription('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <label htmlFor="title" className="text-xs font-bold text-zinc-500 uppercase tracking-widest ml-1">
          Task Title
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-4 py-3 bg-zinc-900/50 border border-white/5 rounded-2xl text-white placeholder-zinc-600 focus:outline-none focus:emerald-border-glow transition-all"
          placeholder="What's on your mind?"
          required
        />
      </div>
      <div className="space-y-2">
        <label htmlFor="description" className="text-xs font-bold text-zinc-500 uppercase tracking-widest ml-1">
          Description (Optional)
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full px-4 py-3 bg-zinc-900/50 border border-white/5 rounded-2xl text-white placeholder-zinc-600 focus:outline-none focus:emerald-border-glow transition-all"
          placeholder="Add some details..."
          rows={3}
        />
      </div>
      <button
        type="submit"
        className="w-full py-3.5 rounded-2xl primary-gradient text-zinc-950 font-bold text-sm emerald-glow hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center space-x-2"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
        </svg>
        <span>Create Task</span>
      </button>
    </form>
  );
}