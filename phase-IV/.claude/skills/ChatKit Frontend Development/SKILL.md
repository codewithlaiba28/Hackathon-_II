---
name: chatkit-frontend-development
description: Build and customize OpenAI ChatKit chat interfaces, including UI components, theming, session management, and domain configuration for production deployments
---

### Purpose
Master the development of conversational interfaces using OpenAI ChatKit, from embedding the chat component to customizing widgets and handling production deployments.

### When to Use
- Building chat-based user interfaces for AI applications
- Implementing conversational task management interfaces
- Creating embeddable chat widgets in Next.js applications
- Deploying production ChatKit implementations

### Core Competencies

**1. Basic ChatKit Integration**
- Embed ChatKit component in Next.js applications
- Configure ChatKit options (theme, appearance, behavior)
- Handle client secret retrieval and session initialization
- Implement session refresh logic
- Manage authentication flow between frontend and backend

**2. Widget Development**
- Create custom widgets using Widget Builder
- Implement ListView components for task displays
- Build interactive cards with status indicators
- Design form widgets for data input
- Create action buttons with custom payloads

**3. Event Handling**
- Implement client-side action handlers
- Build server-side action processors
- Handle form submissions through ChatKit
- Process CustomEvent instances from Web Components
- Chain actions for multi-step workflows

**4. Production Configuration**
- Configure domain allowlist in OpenAI platform
- Generate and manage domain keys
- Set up environment variables (NEXT_PUBLIC_OPENAI_DOMAIN_KEY)
- Deploy to production (Vercel/custom domains)
- Handle CORS and security settings

### Implementation Guidelines

```typescript
// Basic ChatKit setup
import { ChatKit } from '@openai/chatkit';

const config = {
  apiKey: process.env.NEXT_PUBLIC_OPENAI_API_KEY,
  domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY,
  sessionEndpoint: '/api/chatkit/session',
  theme: 'auto',
  appearance: {
    primaryColor: '#0066cc'
  }
};

// Custom widget example
const TaskListWidget = {
  type: 'list',
  items: tasks.map(task => ({
    id: task.id,
    title: task.title,
    status: task.completed ? 'completed' : 'pending',
    actions: ['complete', 'delete']
  }))
};
```

### Common Patterns
- Session management with backend token generation
- Widget streaming for real-time updates
- Action chaining for complex workflows
- Error handling and user feedback
- Responsive design for mobile/desktop

### Resources
- OpenAI ChatKit Documentation
- Domain Allowlist Configuration Guide
- Widget Builder Reference

---