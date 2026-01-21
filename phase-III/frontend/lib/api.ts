import { authClient } from './auth-client';

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || '';

class ApiClient {
  private async request(endpoint: string, options: RequestInit = {}) {
    // Get JWT token from Better Auth
    let token: string | null = null;

    try {
      // Call the /token endpoint to get JWT
      const tokenResponse = await fetch(`${typeof window !== 'undefined' ? window.location.origin : 'http://127.0.0.1:3000'}/api/auth/token`, {
        credentials: 'include',
      });

      if (tokenResponse.ok) {
        const tokenData = await tokenResponse.json();
        token = tokenData.token;
      }
    } catch (error) {
      console.error('Error fetching JWT token:', error);
    }

    if (!token) {
      throw new Error('Unauthorized: No JWT token found');
    }

    // Normalize endpoint - Phase II requires /api/{user_id}/tasks
    const baseUrl = BACKEND_URL.replace(/\/$/, '');
    const url = `${baseUrl}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;

    console.log(`🚀 API Request: ${options.method || 'GET'} ${url}`);

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
          ...options.headers,
        },
      });

      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch (e) {
          console.warn('Could not parse error response');
        }
        throw new Error(errorMessage);
      }

      return response.json();
    } catch (error: any) {
      console.error(`❌ Fetch failed for ${url}:`, error);
      if (error instanceof TypeError && error.message === 'Failed to fetch') {
        console.error('This is likely a CORS error or the backend is not reachable.');
      }
      throw error;
    }
  }

  // Helper to construct path with user_id as per Phase II
  private getPath(userId: string, path: string = '') {
    return `/api/${userId}/tasks${path}`;
  }

  getTasks = async (userId: string) => this.request(this.getPath(userId));

  createTask = async (userId: string, data: any) =>
    this.request(this.getPath(userId), {
      method: 'POST',
      body: JSON.stringify(data)
    });

  updateTask = async (userId: string, taskId: string, data: any) =>
    this.request(this.getPath(userId, `/${taskId}`), {
      method: 'PUT',
      body: JSON.stringify(data)
    });

  toggleTask = async (userId: string, taskId: string) =>
    this.request(this.getPath(userId, `/${taskId}/complete`), {
      method: 'PATCH'
    });

  deleteTask = async (userId: string, taskId: string) =>
    this.request(this.getPath(userId, `/${taskId}`), {
      method: 'DELETE'
    });

  sendChatMessage = async (userId: string, message: string, conversationId?: number) =>
    this.request(`/api/${userId}/chat`, {
      method: 'POST',
      body: JSON.stringify({
        message,
        conversation_id: conversationId
      })
    });
}

export const apiClient = new ApiClient();
export default ApiClient;
