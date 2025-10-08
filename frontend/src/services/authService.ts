import apiClient from './api';

export const login = async (email: string, password: string) => {
  try {
    const response = await apiClient.post('/api/v1.0/login', { email, password });
    return response.data;
  } catch (error) {
    throw error;
  }
};