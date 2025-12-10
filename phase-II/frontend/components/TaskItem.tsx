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

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="bg-gray-700/50 backdrop-blur-sm shadow rounded-lg p-4 mb-3 border border-gray-600">
      {isEditing ? (
        <div className="space-y-3">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 bg-gray-600 text-white border border-gray-500 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
            placeholder="Task title"
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 bg-gray-600 text-white border border-gray-500 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
            placeholder="Task description"
            rows={2}
          />
          <div className="flex space-x-2">
            <button
              onClick={handleUpdate}
              className="px-3 py-1 bg-gradient-to-r from-green-600 to-green-800 text-white rounded-md hover:from-green-700 hover:to-green-900"
            >
              Save
            </button>
            <button
              onClick={handleCancel}
              className="px-3 py-1 bg-gradient-to-r from-gray-600 to-gray-800 text-white rounded-md hover:from-gray-700 hover:to-gray-900"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div className="flex items-start justify-between">
            <div className="flex items-start">
              <input
                type="checkbox"
                checked={task.status === 'completed'}
                onChange={() => onToggle(task.id)}
                className="mt-1 mr-2 h-4 w-4 text-red-500 rounded focus:ring-red-500 bg-gray-600 border-gray-500"
              />
              <div>
                <h3 className={`text-lg font-medium ${task.status === 'completed' ? 'line-through text-gray-400' : 'text-white'}`}>
                  {task.title}
                </h3>
                {task.description && (
                  <p className={`mt-1 ${task.status === 'completed' ? 'line-through text-gray-400' : 'text-gray-300'}`}>
                    {task.description}
                  </p>
                )}
                <p className="text-xs text-gray-400 mt-2">
                  Created: {formatDate(task.created_at)} | Updated: {formatDate(task.updated_at)}
                </p>
              </div>
            </div>
            <div className="flex space-x-1">
              <button
                onClick={() => setIsEditing(true)}
                className="p-1 text-blue-400 hover:text-blue-300"
                title="Edit"
              >
                ✏️
              </button>
              <button
                onClick={() => onDelete(task.id)}
                className="p-1 text-red-400 hover:text-red-300"
                title="Delete"
              >
                🗑️
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}