import TaskItem from './TaskItem';

interface Task {
  id: string;
  title: string;
  description?: string;
  status: string;
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  tasks: Task[];
  onUpdateTask: (id: string, data: { title?: string; description?: string; status?: string }) => void;
  onDeleteTask: (id: string) => void;
  onToggleTask: (id: string) => void;
}

export default function TaskList({ tasks, onUpdateTask, onDeleteTask, onToggleTask }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="bg-gray-800/50 backdrop-blur-sm shadow rounded-lg p-8 text-center border border-gray-700">
        <h3 className="text-lg font-medium text-white">No tasks yet</h3>
        <p className="mt-1 text-gray-300">Get started by adding a new task.</p>
      </div>
    );
  }

  return (
    <div className="bg-gray-800/50 backdrop-blur-sm shadow rounded-lg p-6 border border-gray-700">
      <h2 className="text-xl font-bold text-white mb-4">Your Tasks</h2>
      <div>
        {tasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onUpdate={onUpdateTask}
            onDelete={onDeleteTask}
            onToggle={onToggleTask}
          />
        ))}
      </div>
    </div>
  );
}