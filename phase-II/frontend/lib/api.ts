import { authClient } from './auth-client';

// Use proxy API route to communicate with backend through Better Auth session
const PROXY_BASE_URL = '/api/proxy';

class ApiClient {
  private proxyBaseUrl: string;

  constructor() {
    this.proxyBaseUrl = PROXY_BASE_URL;
  }

  private async request(endpoint: string, options: RequestInit = {}) {
    // Extract the actual backend endpoint from the provided endpoint
    // For example, if endpoint is '/api/tasks/', we need to pass 'api/tasks/' to the proxy
    const backendEndpoint = endpoint.startsWith('/') ? endpoint.substring(1) : endpoint;

    const url = `${this.proxyBaseUrl}?endpoint=${encodeURIComponent(backendEndpoint)}`;

    // Get JWT token from localStorage  
    const jwtToken = typeof window !== 'undefined' ? localStorage.getItem('jwt_token') : null;

    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        // Include JWT token in Authorization: Bearer header (REQUIREMENT 2!)
        ...(jwtToken ? { 'Authorization': `Bearer ${jwtToken}` } : {}),
        ...options.headers,
      },
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

  get = async (endpoint: string) => this.request(endpoint, { method: 'GET' });
  post = async (endpoint: string, data: any) =>
    this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  put = async (endpoint: string, data: any) =>
    this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  delete = async (endpoint: string) => this.request(endpoint, { method: 'DELETE' });
}

export const apiClient = new ApiClient();
export default ApiClient;