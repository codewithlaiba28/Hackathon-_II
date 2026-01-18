import { useState } from 'react';

interface Task {
  id: string;
  title: string;
  description?: string;
  status: string;
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
        <div className="flex items-center space-x-4">
          <button
            onClick={() => onToggle(task.id)}
            className={`w-6 h-6 rounded-lg border-2 flex items-center justify-center transition-all ${isCompleted ? 'bg-primary border-primary text-zinc-950' : 'border-zinc-700 hover:border-primary text-transparent'}`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
            </svg>
          </button>

          <div className="flex-1 min-w-0">
            <h3 className={`font-semibold transition-all ${isCompleted ? 'text-zinc-500 line-through' : 'text-white'}`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`text-sm mt-1 truncate ${isCompleted ? 'text-zinc-600 line-through' : 'text-zinc-400'}`}>
                {task.description}
              </p>
            )}
          </div>

          <div className="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
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