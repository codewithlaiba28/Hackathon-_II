import React, { useState } from 'react';

interface TaskFilterControlsProps {
  onApplyFilters: (filters: {
    status?: string;
    priority?: string;
    tags?: string[];
    due_date_start?: string;
    due_date_end?: string;
    search_query?: string;
    sort_by?: string;
    sort_order?: string;
  }) => void;
  initialFilters?: {
    status?: string;
    priority?: string;
    tags?: string[];
    due_date_start?: string;
    due_date_end?: string;
    search_query?: string;
    sort_by?: string;
    sort_order?: string;
  };
}

const TaskFilterControls: React.FC<TaskFilterControlsProps> = ({ onApplyFilters, initialFilters }) => {
  const [status, setStatus] = useState(initialFilters?.status || 'all');
  const [priority, setPriority] = useState(initialFilters?.priority || '');
  const [tags, setTags] = useState<string[]>(initialFilters?.tags || []);
  const [newTagInput, setNewTagInput] = useState('');
  const [dueDateStart, setDueDateStart] = useState(initialFilters?.due_date_start || '');
  const [dueDateEnd, setDueDateEnd] = useState(initialFilters?.due_date_end || '');
  const [searchQuery, setSearchQuery] = useState(initialFilters?.search_query || '');
  const [sortBy, setSortBy] = useState(initialFilters?.sort_by || '');
  const [sortOrder, setSortOrder] = useState(initialFilters?.sort_order || 'asc');

  const handleApply = () => {
    onApplyFilters({
      status: status === 'all' ? undefined : status,
      priority: priority || undefined,
      tags: tags.length > 0 ? tags : undefined,
      due_date_start: dueDateStart || undefined,
      due_date_end: dueDateEnd || undefined,
      search_query: searchQuery || undefined,
      sort_by: sortBy || undefined,
      sort_order: sortOrder || undefined,
    });
  };

  const handleTagAdd = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && newTagInput.trim() !== '') {
      e.preventDefault();
      setTags([...tags, newTagInput.trim()]);
      setNewTagInput('');
    }
  };

  const handleTagRemove = (tagToRemove: string) => {
    setTags(tags.filter(tag => tag !== tagToRemove));
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '10px', marginBottom: '10px' }}>
      <h3>Filter Tasks</h3>
      <div>
        <label htmlFor="statusFilter">Status:</label>
        <select id="statusFilter" value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="all">All</option>
          <option value="pending">Pending</option>
          <option value="completed">Completed</option>
        </select>
      </div>
      <div>
        <label htmlFor="priorityFilter">Priority:</label>
        <select id="priorityFilter" value={priority} onChange={(e) => setPriority(e.target.value)}>
          <option value="">Any</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
      </div>
      <div>
        <label htmlFor="tagInput">Tags:</label>
        <input
          id="tagInput"
          type="text"
          value={newTagInput}
          onChange={(e) => setNewTagInput(e.target.value)}
          onKeyDown={handleTagAdd}
          placeholder="Add tag and press Enter"
        />
        <div>
          {tags.map((tag, index) => (
            <span key={index} style={{ marginRight: '5px', padding: '2px 5px', border: '1px solid #eee' }}>
              {tag}
              <button onClick={() => handleTagRemove(tag)} style={{ marginLeft: '5px' }}>x</button>
            </span>
          ))}
        </div>
      </div>
      <div>
        <label htmlFor="dueDateStart">Due Date Start:</label>
        <input
          id="dueDateStart"
          type="datetime-local"
          value={dueDateStart}
          onChange={(e) => setDueDateStart(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="dueDateEnd">Due Date End:</label>
        <input
          id="dueDateEnd"
          type="datetime-local"
          value={dueDateEnd}
          onChange={(e) => setDueDateEnd(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="searchQuery">Search:</label>
        <input
          id="searchQuery"
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search title or description"
        />
      </div>
      {/* Sort Controls */}
      <div style={{ marginTop: '10px' }}>
        <label htmlFor="sortBy">Sort By:</label>
        <select id="sortBy" value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="">None</option>
          <option value="title">Title</option>
          <option value="due_date">Due Date</option>
          <option value="priority">Priority</option>
          <option value="created_at">Created At</option>
        </select>
        <label htmlFor="sortOrder" style={{ marginLeft: '10px' }}>Order:</label>
        <select id="sortOrder" value={sortOrder} onChange={(e) => setSortOrder(e.target.value)}>
          <option value="asc">Ascending</option>
          <option value="desc">Descending</option>
        </select>
      </div>
      <button onClick={handleApply}>Apply Filters</button>
    </div>
  );
};

// Placeholder for TaskList component that would consume these filters
const TaskList: React.FC = () => {
  const [filters, setFilters] = useState({});
  const [tasks, setTasks] = useState([]); // Assuming tasks are fetched based on filters

  const applyFilters = (newFilters: any) => {
    setFilters(newFilters);
    // In a real app, you'd fetch tasks from your API here
    console.log("Applying filters:", newFilters);
    // Example: fetchTasks(newFilters).then(setTasks);
  };

  return (
    <div>
      <h1>My Tasks</h1>
      <TaskFilterControls onApplyFilters={applyFilters} initialFilters={filters} />
      {/* Display tasks here */}
      <p>Displaying tasks with current filters: {JSON.stringify(filters)}</p>
      {tasks.length === 0 && <p>No tasks found.</p>}
      {/* {tasks.map(task => <TaskItem key={task.id} task={task} />)} */}
    </div>
  );
};

export default TaskList;
