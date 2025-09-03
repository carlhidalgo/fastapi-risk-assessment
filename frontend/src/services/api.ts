import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth APIs
export const authApi = {
  login: async (email: string, password: string) => {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  },
  
  register: async (email: string, password: string) => {
    const response = await api.post('/auth/register', { email, password });
    return response.data;
  },
  
  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  }
};

// Companies APIs
export const companiesApi = {
  getAll: async (page: number = 1, search?: string) => {
    const params = new URLSearchParams({ page: page.toString() });
    if (search) params.append('search', search);
    
    const response = await api.get(`/companies?${params}`);
    return response.data;
  },
  
  create: async (company: { name: string; industry: string; size: string }) => {
    const response = await api.post('/companies', company);
    return response.data;
  }
};

// Requests APIs
export const requestsApi = {
  getAll: async (page: number = 1, search?: string) => {
    const params = new URLSearchParams({ page: page.toString() });
    if (search) params.append('search', search);
    
    const response = await api.get(`/requests?${params}`);
    return response.data;
  },
  
  create: async (request: {
    company_id: string;
    amount: number;
    purpose: string;
    risk_inputs: any;
  }) => {
    const response = await api.post('/requests', request);
    return response.data;
  }
};

export default api;
