'use client';

import { useState } from 'react';

interface Task {
  id: string;
  title: string;
  description?: string;
  status: string;
  priority?: string;
  due_date?: string;
  is_recurring?: boolean;
  recurrence_pattern?: string;
  tags?: any[]; // Keep flexible as backend returns object list or frontend might expect strings
  created_at: string;
  updated_at: string;
}

interface TaskItemProps {
  task: Task;
  onUpdate: (id: string, data: { title?: string; description?: string; status?: string }) => void;
  onDelete: (id: string) => void;
  onToggle: (id: string) => void;
}

export default function TaskItem({ task, onUpdate, onDelete, onToggle }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');

  const handleUpdate = () => {
    onUpdate(task.id, { title, description });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setTitle(task.title);
    setDescription(task.description || '');
    setIsEditing(false);
  };

  const isCompleted = task.status === 'completed';

  const getPriorityColor = (p?: string) => {
    switch (p?.toLowerCase()) {
      case 'high': return 'bg-red-500/20 text-red-500 border-red-500/20';
      case 'medium': return 'bg-yellow-500/20 text-yellow-500 border-yellow-500/20';
      case 'low': return 'bg-blue-500/20 text-blue-500 border-blue-500/20';
      default: return 'bg-zinc-500/20 text-zinc-500 border-zinc-500/20';
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return null;
    return new Date(dateString).toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`group glass-morphism p-5 rounded-2xl border transition-all duration-300 ${isCompleted ? 'border-primary/10 opacity-70' : 'border-white/5 hover:border-primary/30'}`}>
      {isEditing ? (
        <div className="space-y-4">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-4 py-2 bg-zinc-900 border border-white/10 rounded-xl text-white focus:outline-none focus:border-primary"
            placeholder="Task title"
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-4 py-2 bg-zinc-900 border border-white/10 rounded-xl text-white focus:outline-none focus:border-primary"
            placeholder="Task description"
            rows={2}
          />
          <div className="flex space-x-2 justify-end">
            <button
              onClick={handleCancel}
              className="px-4 py-2 bg-zinc-800 text-zinc-400 rounded-xl hover:text-white transition-colors text-sm font-medium"
            >
              Cancel
            </button>
            <button
              onClick={handleUpdate}
              className="px-4 py-2 primary-gradient text-zinc-950 rounded-xl font-bold text-sm emerald-glow"
            >
              Update Task
            </button>
          </div>
        </div>
      ) : (
        <div className="flex items-start space-x-4">
          <button
            onClick={() => onToggle(task.id)}
            className={`w-6 h-6 mt-1 rounded-lg border-2 flex items-center justify-center transition-all ${isCompleted ? 'bg-primary border-primary text-zinc-950' : 'border-zinc-700 hover:border-primary text-transparent'}`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
            </svg>
          </button>

          <div className="flex-1 min-w-0">
            <div className="flex items-center space-x-2 mb-1">
              {task.priority && (
                <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border ${getPriorityColor(task.priority)}`}>
                  {task.priority}
                </span>
              )}
              {task.is_recurring && (
                <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border bg-purple-500/20 text-purple-500 border-purple-500/20 flex items-center gap-1">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
                  </svg>
                  {task.recurrence_pattern}
                </span>
              )}
            </div>

            <h3 className={`font-semibold text-lg transition-all ${isCompleted ? 'text-zinc-500 line-through' : 'text-white'}`}>
              {task.title}
            </h3>

            {task.description && (
              <p className={`text-sm mt-1 mb-2 ${isCompleted ? 'text-zinc-600 line-through' : 'text-zinc-400'}`}>
                {task.description}
              </p>
            )}

            <div className="flex flex-wrap gap-2 mt-3 items-center">
              {task.due_date && (
                <div className={`flex items-center space-x-1 text-xs px-2 py-1 rounded-md ${new Date(task.due_date) < new Date() && !isCompleted ? 'bg-red-500/10 text-red-400' : 'bg-zinc-800 text-zinc-400'}`}>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
                  </svg>
                  <span>{formatDate(task.due_date)}</span>
                </div>
              )}

              {task.tags && task.tags.map((tagObj: any, idx: number) => {
                const tagName = typeof tagObj === 'string' ? tagObj : tagObj.tag;
                return (
                  <span key={idx} className="text-xs px-2 py-1 rounded-md bg-zinc-800 text-zinc-400 border border-white/5">
                    #{tagName}
                  </span>
                );
              })}
            </div>
          </div>

          <div className="flex flex-col space-y-2 opacity-0 group-hover:opacity-100 transition-opacity">
            <button
              onClick={() => setIsEditing(true)}
              className="p-2 text-zinc-500 hover:text-primary transition-colors hover:bg-primary/10 rounded-lg"
              title="Edit"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
            </button>
            <button
              onClick={() => onDelete(task.id)}
              className="p-2 text-zinc-500 hover:text-red-500 transition-colors hover:bg-red-500/10 rounded-lg"
              title="Delete"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}