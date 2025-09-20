import apiClient from './api';

export const getRoleList = async (searchValue: string, page: number, perPage: number) => {
    const response = await apiClient.get('/api/v1.0/accounts/roles', { params: { search_value: searchValue, page, per_page: perPage } });
    return response.data;
};
export const getSimpleRoles = async (searchValue: string, roleIds: string, page: number, perPage: number) => {
    const response = await apiClient.get('/api/v1.0/accounts/simple_roles', { params: { search_value: searchValue, role_ids: roleIds, page, per_page: perPage } });
    return response.data;
};
export const deleteRole = async (roleId: string) => {
    const response = await apiClient.delete(`/api/v1.0/accounts/roles/${roleId}`);
    return response.data;
};

export const addRole = async (name: string, description: string) => {
    const response = await apiClient.post('/api/v1.0/accounts/roles', { name, description });
    return response.data;
};
export const updateRole = async (roleId: string, name: string, description: string) => {
    const response = await apiClient.patch(`/api/v1.0/accounts/roles/${roleId}`, { name, description });
    return response.data;
}

export const getRoleDetail = async (roleId: string) => {
    const response = await apiClient.get(`/api/v1.0/accounts/roles/${roleId}`);
    return response.data;
};

export const addRoleUser = async (roleId: string, userIds: string[]) => {
    const response = await apiClient.post(`/api/v1.0/accounts/roles/${roleId}/users`, { user_ids: userIds });
    return response.data;
}

export const deleteRoleUser = async (roleId: string, userIds: string[]) => {
    const response = await apiClient.delete(`/api/v1.0/accounts/roles/${roleId}/users`, { data: { user_ids: userIds } });
    return response.data;
}

export const getRoleUserList = async (roleId: string, searchValue: string, page: number, perPage: number) => {
    const response = await apiClient.get(`/api/v1.0/accounts/roles/${roleId}/users`, { params: { search_value: searchValue, page, per_page: perPage } });
    return response.data;
}