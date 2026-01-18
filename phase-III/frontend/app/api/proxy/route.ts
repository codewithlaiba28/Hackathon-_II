// frontend/app/api/proxy/route.ts
import { NextRequest } from 'next/server';
import { auth } from '@/lib/better-auth';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const backendEndpoint = searchParams.get('endpoint');

  if (!backendEndpoint) {
    return Response.json({ error: 'Backend endpoint not specified' }, { status: 400 });
  }

  try {
    // Get JWT token from request header (passed from frontend)
    const authHeader = request.headers.get('Authorization');
    let jwtToken = authHeader?.replace('Bearer ', '');

    // If no token in header, try to get from cookie or return error
    if (!jwtToken) {
      return Response.json({ error: 'No authentication token provided' }, { status: 401 });
    }

    // Make request to backend with JWT token
    const backendResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/${backendEndpoint}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${jwtToken}`,
        'Content-Type': 'application/json',
      },
    });

    const data = await backendResponse.json();
    return Response.json(data, { status: backendResponse.status });
  } catch (error) {
    console.error('Proxy GET error:', error);
    return Response.json({ error: 'Backend request failed' }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const backendEndpoint = searchParams.get('endpoint');

  if (!backendEndpoint) {
    return Response.json({ error: 'Backend endpoint not specified' }, { status: 400 });
  }

  try {
    const contentType = request.headers.get('Content-Type') || 'application/json';
    let body;

    // Handle different content types for the body
    if (contentType.includes('application/x-www-form-urlencoded')) {
      body = await request.text();
    } else {
      const jsonBody = await request.json();
      body = JSON.stringify(jsonBody);
    }

    const authHeader = request.headers.get('Authorization');
    let jwtToken = authHeader?.replace('Bearer ', '');

    // Allow login and signup without a token
    const isPublicEndpoint = backendEndpoint.includes('api/auth/login') || backendEndpoint.includes('api/auth/signup');

    if (!jwtToken && !isPublicEndpoint) {
      return Response.json({ error: 'No authentication token provided' }, { status: 401 });
    }

    const headers: Record<string, string> = {
      'Content-Type': contentType,
    };

    if (jwtToken) {
      headers['Authorization'] = `Bearer ${jwtToken}`;
    }

    const backendResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/${backendEndpoint}`, {
      method: 'POST',
      headers,
      body,
    });

    const data = await backendResponse.json();
    return Response.json(data, { status: backendResponse.status });
  } catch (error) {
    console.error('Proxy POST error:', error);
    return Response.json({ error: 'Backend request failed' }, { status: 500 });
  }
}


export async function PUT(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const backendEndpoint = searchParams.get('endpoint');

  if (!backendEndpoint) {
    return Response.json({ error: 'Backend endpoint not specified' }, { status: 400 });
  }

  try {
    const body = await request.json();
    const authHeader = request.headers.get('Authorization');
    let jwtToken = authHeader?.replace('Bearer ', '');

    if (!jwtToken) {
      return Response.json({ error: 'No authentication token provided' }, { status: 401 });
    }

    const backendResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/${backendEndpoint}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${jwtToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    const data = await backendResponse.json();
    return Response.json(data, { status: backendResponse.status });
  } catch (error) {
    console.error('Proxy PUT error:', error);
    return Response.json({ error: 'Backend request failed' }, { status: 500 });
  }
}

export async function DELETE(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const backendEndpoint = searchParams.get('endpoint');

  if (!backendEndpoint) {
    return Response.json({ error: 'Backend endpoint not specified' }, { status: 400 });
  }

  try {
    const authHeader = request.headers.get('Authorization');
    let jwtToken = authHeader?.replace('Bearer ', '');

    if (!jwtToken) {
      return Response.json({ error: 'No authentication token provided' }, { status: 401 });
    }

    const backendResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/${backendEndpoint}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${jwtToken}`,
        'Content-Type': 'application/json',
      },
    });

    const data = await backendResponse.json();
    return Response.json(data, { status: backendResponse.status });
  } catch (error) {
    console.error('Proxy DELETE error:', error);
    return Response.json({ error: 'Backend request failed' }, { status: 500 });
  }
}