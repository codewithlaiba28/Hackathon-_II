'use client';

import { useState } from 'react';

interface TaskFormProps {
  onAddTask: (taskData: {
    title: string;
    description?: string;
    priority: string;
    due_date?: string;
    is_recurring: boolean;
    recurrence_pattern?: string;
    tags?: string[];
  }) => void;
}

export default function TaskForm({ onAddTask }: TaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('medium');
  const [dueDate, setDueDate] = useState('');
  const [isRecurring, setIsRecurring] = useState(false);
  const [recurrencePattern, setRecurrencePattern] = useState('daily');
  const [tags, setTags] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (title.trim()) {
      onAddTask({
        title: title.trim(),
        description: description.trim() || undefined,
        priority,
        due_date: dueDate || undefined,
        is_recurring: isRecurring,
        recurrence_pattern: isRecurring ? recurrencePattern : undefined,
        tags: tags.split(',').map(t => t.trim()).filter(Boolean)
      });
      // Reset form
      setTitle('');
      setDescription('');
      setPriority('medium');
      setDueDate('');
      setIsRecurring(false);
      setRecurrencePattern('daily');
      setTags('');
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

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="space-y-2">
          <label htmlFor="priority" className="text-xs font-bold text-zinc-500 uppercase tracking-widest ml-1">
            Priority
          </label>
          <select
            id="priority"
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            className="w-full px-4 py-3 bg-zinc-900/50 border border-white/5 rounded-2xl text-white focus:outline-none focus:emerald-border-glow transition-all appearance-none"
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div className="space-y-2 md:col-span-2">
          <label htmlFor="dueDate" className="text-xs font-bold text-zinc-500 uppercase tracking-widest ml-1">
            Due Date
          </label>
          <input
            type="datetime-local"
            id="dueDate"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            className="w-full px-4 py-3 bg-zinc-900/50 border border-white/5 rounded-2xl text-white placeholder-zinc-600 focus:outline-none focus:emerald-border-glow transition-all"
          />
        </div>
      </div>

      <div className="space-y-2">
        <label htmlFor="tags" className="text-xs font-bold text-zinc-500 uppercase tracking-widest ml-1">
          Tags (comma separated)
        </label>
        <input
          type="text"
          id="tags"
          value={tags}
          onChange={(e) => setTags(e.target.value)}
          className="w-full px-4 py-3 bg-zinc-900/50 border border-white/5 rounded-2xl text-white placeholder-zinc-600 focus:outline-none focus:emerald-border-glow transition-all"
          placeholder="work, urgent, personal"
        />
      </div>

      <div className="flex items-center space-x-3 bg-zinc-900/30 p-3 rounded-2xl border border-white/5">
        <input
          type="checkbox"
          id="isRecurring"
          checked={isRecurring}
          onChange={(e) => setIsRecurring(e.target.checked)}
          className="w-5 h-5 rounded border-white/10 bg-zinc-900 text-emerald-500 focus:ring-emerald-500 focus:ring-offset-0"
        />
        <label htmlFor="isRecurring" className="text-sm font-medium text-zinc-300 select-none cursor-pointer flex-1">
          Recurring Task
        </label>

        {isRecurring && (
          <select
            value={recurrencePattern}
            onChange={(e) => setRecurrencePattern(e.target.value)}
            className="px-3 py-1 bg-zinc-800 border border-white/10 rounded-xl text-white text-sm focus:outline-none"
          >
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </select>
        )}
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