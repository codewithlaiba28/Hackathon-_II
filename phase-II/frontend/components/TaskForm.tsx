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
    <div className="bg-gray-800/50 backdrop-blur-sm shadow rounded-lg p-6 mb-6 border border-gray-700">
      <h2 className="text-xl font-bold text-white mb-4">Add New Task</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-200 mb-1">
            Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 bg-gray-700 text-white border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
            placeholder="What needs to be done?"
            required
          />
        </div>
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-200 mb-1">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 bg-gray-700 text-white border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
            placeholder="Add details..."
            rows={2}
          />
        </div>
        <button
          type="submit"
          className="w-full bg-gradient-to-r from-red-600 to-red-800 text-white py-2 px-4 rounded-md hover:from-red-700 hover:to-red-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
        >
          Add Task
        </button>
      </form>
    </div>
  );
}