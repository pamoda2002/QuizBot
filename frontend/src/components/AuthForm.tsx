/**
 * Authentication Form Component
 * Handles user signup and login
 */
'use client';

import { useState } from 'react';
import { apiService } from '@/services/api';
import { SignupRequest, LoginRequest } from '@/types';

interface AuthFormProps {
  onAuthSuccess: () => void;
}

export default function AuthForm({ onAuthSuccess }: AuthFormProps) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      if (isLogin) {
        // Login
        const loginData: LoginRequest = { email, password };
        await apiService.login(loginData);
      } else {
        // Signup
        if (!username.trim()) {
          setError('Username is required');
          setIsLoading(false);
          return;
        }
        const signupData: SignupRequest = { email, username, password };
        await apiService.signup(signupData);
      }
      
      // Call success callback
      onAuthSuccess();
    } catch (err: any) {
      // Format error message properly
      let errorMessage = 'Authentication failed. Please try again.';
      
      if (err.response?.data?.detail) {
        const detail = err.response.data.detail;
        if (Array.isArray(detail)) {
          // Pydantic validation errors - format as readable text
          errorMessage = detail.map((e: any) => {
            if (e.msg && e.msg.includes('email')) {
              return 'Please enter a valid email address (e.g., yourname@gmail.com)';
            }
            const field = e.loc ? e.loc[e.loc.length - 1] : 'Field';
            return `${field}: ${e.msg || 'Invalid input'}`;
          }).join('. ');
        } else if (typeof detail === 'string') {
          errorMessage = detail;
        } else {
          errorMessage = JSON.stringify(detail);
        }
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleMode = () => {
    setIsLogin(!isLogin);
    setError('');
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-brand">
          <div className="brand-icon">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="48" height="48" rx="12" fill="url(#gradient1)"/>
              <path d="M24 12L32 18V30L24 36L16 30V18L24 12Z" fill="white" fillOpacity="0.9"/>
              <defs>
                <linearGradient id="gradient1" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse">
                  <stop stopColor="#3B82F6"/>
                  <stop offset="1" stopColor="#2563EB"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h1 className="brand-title">QUIZBOT</h1>
          <p className="brand-subtitle">Intelligent Assessment Platform</p>
        </div>

        <div className="auth-card">
          <div className="auth-header">
            <h2 className="auth-title">
              {isLogin ? 'Account Login' : 'Create New Account'}
            </h2>
            <p className="auth-description">
              {isLogin 
                ? 'Enter your credentials to access your account' 
                : 'Register to start your learning journey'}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-group">
              <label htmlFor="email" className="form-label">
                Email Address
              </label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="form-input"
                placeholder="name@example.com"
                autoComplete="email"
              />
              <p className="form-hint" style={{ fontSize: '0.75rem', color: '#6b7280', marginTop: '0.25rem' }}>
                Use a complete email (e.g., yourname@gmail.com)
              </p>
            </div>

            {!isLogin && (
              <div className="form-group">
                <label htmlFor="username" className="form-label">
                  Display Name
                </label>
                <input
                  id="username"
                  type="text"
                  required={!isLogin}
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="form-input"
                  placeholder="John Doe"
                  autoComplete="name"
                />
              </div>
            )}

            <div className="form-group">
              <label htmlFor="password" className="form-label">
                Password
              </label>
              <input
                id="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="form-input"
                placeholder="••••••••"
                minLength={6}
                autoComplete={isLogin ? "current-password" : "new-password"}
              />
              {!isLogin && (
                <p className="form-hint">Minimum 6 characters required</p>
              )}
            </div>

            {error && (
              <div className="error-message">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
                </svg>
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="auth-submit-btn"
            >
              {isLoading ? (
                <>
                  <svg className="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                  </svg>
                  Processing...
                </>
              ) : (
                isLogin ? 'Login to Account' : 'Create Account'
              )}
            </button>
          </form>

          <div className="auth-footer">
            <div className="divider">
              <span>or</span>
            </div>
            <button
              onClick={toggleMode}
              className="toggle-mode-btn"
            >
              {isLogin 
                ? "Don't have an account? Create one" 
                : 'Already have an account? Login'}
            </button>
          </div>
        </div>

        <div className="auth-info">
          <p className="info-text">
            © 2026 QuizBot. Secure authentication powered by advanced encryption.
          </p>
        </div>
      </div>
    </div>
  );
}
