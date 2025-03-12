import apiClient from './api';

export const updateMyProfile = async (lang: string) => {
  try {
    const response = await apiClient.patch('/api/v1.0/accounts/my_profile', { lang });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getMyProfile = async () => {
  try {
    const response = await apiClient.get('/api/v1.0/accounts/my_profile');
    return response.data;
  } catch (error) {
    throw error;
  }
};