import apiClient from './api';

export const getApplicationList = async (searchValue: string, page: number, perPage: number, type: string) => {
  const response = await apiClient.get('/api/v1.0/accounts/applications', { params: { search_value: searchValue, page: page + 1, per_page: perPage, type } });
  return response.data;
};
export const getSimpletApplicationList = async (searchValue: string, appIds: string, page: number, perPage: number, type: string) => {
  const response = await apiClient.get('/api/v1.0/accounts/simple_applications', { params: { search_value: searchValue, app_ids: appIds, page, per_page: perPage, type } });
  return response.data;
};


export const addApplication = async (name: string, description: string, type: string) => {
  const response = await apiClient.post('/api/v1.0/accounts/applications', { name, description, type });
  return response.data
};
export const updateApplication = async (id: string, name: string, description: string, type: string) => {
  const response = await apiClient.patch('/api/v1.0/accounts/applications', { name, description, type });
  return response.data
};

export const getApplicationDetail = async (applicationId: string) => {
  const response = await apiClient.get(`/api/v1.0/accounts/applications/${applicationId}`);
  return response.data
};

export const delApplicationDetail = async (applicationId: string) => {
  const response = await apiClient.delete(`/api/v1.0/accounts/applications/${applicationId}`);
  return response.data
};


