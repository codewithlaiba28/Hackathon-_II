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
      <div className="glass-morphism rounded-3xl p-12 text-center border border-white/5">
        <div className="w-16 h-16 bg-zinc-900 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-white/5">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-zinc-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <h3 className="text-xl font-bold text-white mb-2">No tasks found</h3>
        <p className="text-zinc-500 max-w-xs mx-auto">Your task list is empty. Start by adding a new task from the sidebar.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
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
  );
}