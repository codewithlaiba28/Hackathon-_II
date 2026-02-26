import React, { useState } from 'react';

interface TaskFormProps {
  initialData?: {
    title?: string;
    description?: string;
    is_recurring?: boolean;
    recurring_frequency?: string;
    due_date?: string;
    priority?: string;
    tags?: string[];
    // ... other task fields
  };
  onSubmit: (data: any) => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ initialData, onSubmit }) => {
  const [title, setTitle] = useState(initialData?.title || '');
  const [description, setDescription] = useState(initialData?.description || '');
  const [isRecurring, setIsRecurring] = useState(initialData?.is_recurring || false);
  const [recurringFrequency, setRecurringFrequency] = useState(initialData?.recurring_frequency || '');
  const [dueDate, setDueDate] = useState<Date | undefined>(initialData?.due_date ? new Date(initialData.due_date) : undefined);
  const [priority, setPriority] = useState(initialData?.priority || 'Medium');
  const [tags, setTags] = useState<string[]>(initialData?.tags || []); // New state for tags
  const [newTag, setNewTag] = useState(''); // State for the new tag input
  // ... state for other task fields

  const handleSubmit = async (e: React.FormEvent) => { // Made async
    e.preventDefault();
    const taskData = {
      title,
      description,
      due_date: dueDate?.toISOString(),
      priority,
      tags, // Added tags
      is_recurring: isRecurring,
      recurring_frequency: isRecurring ? recurringFrequency : null,
      // ... other task fields
    };
    onSubmit(taskData);

    // Call set_reminder MCP tool if due_date is set
    if (dueDate) {
      // Assuming a global API client 'api' that can call backend MCP tools
      // In a real app, this would be an actual API call to your backend endpoint
      console.log(`Frontend: Simulating call to set_reminder for task with due_date: ${dueDate.toISOString()}`);
      // await api.set_reminder(task_id, dueDate.toISOString()); // Example API call
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="title">Title:</label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="description">Description:</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>
      {/* Priority Select */}
      <div>
        <label htmlFor="priority">Priority:</label>
        <select
          id="priority"
          value={priority}
          onChange={(e) => setPriority(e.target.value)}
        >
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
      </div>
      {/* Tags Input */}
      <div>
        <label htmlFor="tags">Tags:</label>
        <input
          id="tags"
          type="text"
          value={newTag}
          onChange={(e) => setNewTag(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && newTag.trim() !== '') {
              e.preventDefault();
              setTags([...tags, newTag.trim()]);
              setNewTag('');
            }
          }}
          placeholder="Add a tag and press Enter"
        />
        <div>
          {tags.map((tag, index) => (
            <span key={index} style={{ marginRight: '5px', padding: '2px 5px', border: '1px solid #ccc' }}>
              {tag}
              <button type="button" onClick={() => setTags(tags.filter((_, i) => i !== index))}>
                x
              </button>
            </span>
          ))}
        </div>
      </div>
      {/* Due Date Input */}
      <div>
        <label htmlFor="dueDate">Due Date:</label>
        <input
          id="dueDate"
          type="datetime-local" // HTML5 datetime-local input, can be enhanced with a library
          value={dueDate ? dueDate.toISOString().slice(0, 16) : ''} // Format for datetime-local
          onChange={(e) => setDueDate(e.target.value ? new Date(e.target.value) : undefined)}
        />
      </div>
      <div>
        <label>
          <input
            type="checkbox"
            checked={isRecurring}
            onChange={(e) => setIsRecurring(e.target.checked)}
          />
          Is Recurring?
        </label>
      </div>
      {isRecurring && (
        <div>
          <label htmlFor="recurringFrequency">Recurrence Frequency:</label>
          <select
            id="recurringFrequency"
            value={recurringFrequency}
            onChange={(e) => setRecurringFrequency(e.target.value)}
            required={isRecurring}
          >
            <option value="">Select frequency</option>
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
            <option value="yearly">Yearly</option>
          </select>
        </div>
      )}
      {/* ... other input fields for task properties */}
      <button type="submit">Save Task</button>
    </form>
  );
};

export default TaskForm;
