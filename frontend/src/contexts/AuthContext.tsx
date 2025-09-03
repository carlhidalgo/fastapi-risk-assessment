import React, { createContext, useContext, useState, useEffect } from 'react';
import { AuthContextType, AuthProviderProps, User } from '../types/auth';
import { AuthService } from '../services/authService';
import { parseErrorMessage } from '../utils/errorHandler';
import { AUTH_CONFIG } from '../constants/config';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem(AUTH_CONFIG.TOKEN_KEY));
  const [loading, setLoading] = useState(true);

  const isAuthenticated = !!token && !!user;

  useEffect(() => {
    AuthService.setAuthToken(token);
  }, [token]);

  useEffect(() => {
    const checkAuth = async () => {
      if (token) {
        try {
          const userData = await AuthService.getCurrentUser();
          setUser(userData);
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
      const loginResponse = await AuthService.login({ email, password });
      const { access_token } = loginResponse;
      
      setToken(access_token);
      localStorage.setItem(AUTH_CONFIG.TOKEN_KEY, access_token);

      AuthService.setAuthToken(access_token);
      const userData = await AuthService.getCurrentUser();
      setUser(userData);
    } catch (error: any) {
      console.error('Login failed:', error);
      const errorMessage = parseErrorMessage(error);
      const customError = new Error(errorMessage);
      (customError as any).response = { data: { detail: errorMessage } };
      throw customError;
    }
  };

  const register = async (name: string, email: string, password: string) => {
    try {
      await AuthService.register({ name, email, password });
      await login(email, password);
    } catch (error: any) {
      console.error('Registration failed:', error);
      const errorMessage = parseErrorMessage(error);
      const customError = new Error(errorMessage);
      (customError as any).response = { data: { detail: errorMessage } };
      throw customError;
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem(AUTH_CONFIG.TOKEN_KEY);
    AuthService.setAuthToken(null);
  };

  const value: AuthContextType = {
    user,
    token,
    isAuthenticated,
    loading,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
