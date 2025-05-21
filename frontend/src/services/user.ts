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

export const deleteUser = async (userId: string) => {
  try {
    const response = await apiClient.delete(`/api/v1.0/accounts/users/${userId}`);
    return response.data;
  } catch (error) {
    throw error;
  }
}


export const getUserDetail = async (userId: string) => {
  try {
    const response = await apiClient.get(`/api/v1.0/accounts/users/${userId}`);
    return response.data;
  } catch (error) {
    throw error;
  }
}

export const addUser = async (user: any) => {
  try {
    const response = await apiClient.post('/api/v1.0/accounts/users', user);
    return response.data;
  } catch (error) {
    throw error;
  }
}
export const updateUser = async (userId: string, user: any) => {
  try {
    const response = await apiClient.patch(`/api/v1.0/accounts/users/${userId}`, user);
    return response.data;
  } catch (error) {
    throw error;
  }
}

export const resetUserPassword = async (userId: string) => {
  try {
    const response = await apiClient.post(`/api/v1.0/accounts/users/${userId}/reset_password`);
    return response.data;
  } catch (error) {
    throw error;
  }
}