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

export const getSimpleUser = async (searchValue: string = '') => {
  try {
    const response = await apiClient.get('/api/v1.0/accounts/simple_users', {
      params: {
        search_value: searchValue,
        per_page: 100
      },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
}

export const getUsers = async (searchValue: string = '', deptId: string = '', page: number = 1, perPage: number = 10) => {
  try {
    const response = await apiClient.get('/api/v1.0/accounts/users', {
      params: {
        search_value: searchValue,
        dept_id: deptId,
        per_page: perPage,
        page: page,
      },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
}