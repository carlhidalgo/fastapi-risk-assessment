import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';

interface User {
  id: string;
  email: string;
  name: string;
  is_active: boolean;
  created_at: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

const API_BASE_URL = 'http://localhost:8003/api/v1';

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  const isAuthenticated = !!token && !!user;

  // Set up axios interceptor for authentication
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token]);

  // Check if user is authenticated on app start
  useEffect(() => {
    const checkAuth = async () => {
      if (token) {
        try {
          const response = await axios.get<User>(`${API_BASE_URL}/auth/me`);
          setUser(response.data);
        } catch (error) {
          console.error('Authentication check failed:', error);
          logout();
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, [token]);

  const login = async (email: string, password: string) => {
    try {
      const response = await axios.post<LoginResponse>(`${API_BASE_URL}/auth/login`, {
        email,
        password,
      });

      const { access_token } = response.data;
      setToken(access_token);
      localStorage.setItem('token', access_token);

      // Get user info
      const userResponse = await axios.get<User>(`${API_BASE_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${access_token}` },
      });
      setUser(userResponse.data);
    } catch (error: any) {
      console.error('Login failed:', error);
      
      // Handle different types of errors
      let errorMessage = 'Login failed. Please try again.';
      
      if (error.response?.data) {
        const errorData = error.response.data;
        
        // Handle validation errors (array of error objects)
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail
            .map((err: any) => err.msg || err.message || 'Validation error')
            .join(', ');
        } 
        // Handle simple string errors
        else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
        // Handle general error objects
        else if (errorData.message) {
          errorMessage = errorData.message;
        }
      }
      
      const customError = new Error(errorMessage);
      (customError as any).response = { data: { detail: errorMessage } };
      throw customError;
    }
  };

  const register = async (email: string, password: string) => {
    try {
      await axios.post(`${API_BASE_URL}/auth/register`, {
        email,
        password,
      });

      // Auto-login after registration
      await login(email, password);
    } catch (error: any) {
      console.error('Registration failed:', error);
      
      // Handle different types of errors
      let errorMessage = 'Registration failed. Please try again.';
      
      if (error.response?.data) {
        const errorData = error.response.data;
        
        // Handle validation errors (array of error objects)
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail
            .map((err: any) => err.msg || err.message || 'Validation error')
            .join(', ');
        } 
        // Handle simple string errors
        else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
        // Handle general error objects
        else if (errorData.message) {
          errorMessage = errorData.message;
        }
      }
      
      const customError = new Error(errorMessage);
      (customError as any).response = { data: { detail: errorMessage } };
      throw customError;
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
  };

  const value: AuthContextType = {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
