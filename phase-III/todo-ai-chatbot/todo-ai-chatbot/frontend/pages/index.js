// pages/index.js
import React from 'react';
import ChatInterface from '../components/ChatInterface';
import LoginPage from '../components/LoginPage';
import { useAuth } from '../contexts/AuthContext';

export default function Home() {
  const { user, loading, logout } = useAuth();

  if (loading) {
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>Loading...</div>;
  }

  if (!user) {
    return <LoginPage />;
  }

  return (
    <div className="container">
      <header>
        <div className="header-content">
          <div className="title-area">
            <h1>AI Todo Chatbot</h1>
            <p className="user-info">Logged in as {user.name}</p>
          </div>
          <button className="logout-btn" onClick={logout}>Logout</button>
        </div>
      </header>

      <main>
        <ChatInterface />
      </main>

      <style jsx global>{`
        body {
          margin: 0;
          padding: 0;
          font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen,
            Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
          background-color: #f5f5f5;
        }

        .container {
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
        }

        .header-content {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 30px;
          padding-bottom: 20px;
          border-bottom: 1px solid #eee;
        }
        .title-area h1 {
          font-size: 24px;
          color: #1a1a1a;
          margin: 0;
        }
        .user-info {
          font-size: 14px;
          color: #666;
          margin: 4px 0 0 0;
        }
        .logout-btn {
          padding: 8px 16px;
          border: 1px solid #ddd;
          border-radius: 6px;
          background: white;
          color: #666;
          cursor: pointer;
          font-size: 14px;
          transition: all 0.2s;
        }
        .logout-btn:hover {
          background: #f5f5f5;
          color: #333;
        }
      `}</style>
    </div>
  );
}