import { getToken } from './auth';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  private async request(endpoint: string, options: RequestInit = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const token = getToken();

    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (token) {
      (headers as any)['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      // Try to parse the error response body
      let errorMessage = `HTTP error! status: ${response.status}`;
      try {
        const errorData = await response.json();
        if (errorData && errorData.detail) {
          errorMessage = errorData.detail;
        }
      } catch (e) {
        // If we can't parse the error response, use the status code
        console.warn('Could not parse error response:', e);
      }
      throw new Error(errorMessage);
    }

    return response.json();
  }

  get = (endpoint: string) => this.request(endpoint, { method: 'GET' });
  post = (endpoint: string, data: any) =>
    this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  put = (endpoint: string, data: any) =>
    this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  delete = (endpoint: string) => this.request(endpoint, { method: 'DELETE' });

  // Authentication methods
  login = (email: string, password: string) =>
    this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });

  signup = (email: string, password: string, name?: string) =>
    this.request('/api/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password, name })
    });

  logout = (token: string) =>
    this.request('/api/auth/logout', {
      method: 'POST',
      body: JSON.stringify({ token })
    });
}

export const apiClient = new ApiClient();
export default ApiClient;