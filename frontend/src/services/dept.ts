import apiClient from './api';

export interface DepartmentResponse {
    code: number;
    msg: string;
    data: {
        deptList: any[];
    };
}

/**
 * 获取部门树数据
 * @param searchValue 搜索关键字
 * @param parentDeptId 父部门ID
 * @returns 部门树数据
 */
export const getDeptTree = async (isSimple: boolean): Promise<DepartmentResponse> => {
    try {
        const response = await apiClient.get('/api/v1.0/accounts/depts_tree', {
            params: {
                is_simple: isSimple,
            }
        });
        return response.data;
    } catch (error) {
        throw error;
    }
};

/**
 * 获取简化版部门树数据（不包含领导和审批人信息）
 * @param searchValue 搜索关键字
 * @param parentDeptId 父部门ID
 * @returns 简化版部门树数据
 */
export const getSimpleDeptTree = async (searchValue: string = '', parentDeptId: number = 0): Promise<DepartmentResponse> => {
    try {
        const params = new URLSearchParams();
        if (searchValue) params.append('search_value', searchValue);
        if (parentDeptId) params.append('parent_dept_id', parentDeptId.toString());

        const queryString = params.toString() ? `?${params.toString()}` : '';
        const response = await apiClient.get(`/api/v1.0/accounts/simple_depts_tree${queryString}`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const addDept = async (name: string, parentDeptId: string, leaderId: string, approverIdList: string[]) => {
    try {
        const response = await apiClient.post('/api/v1.0/accounts/depts', {
            name,
            parent_dept_id: parentDeptId,
            leader_id: leaderId,
            approver_id_list: approverIdList
        });
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const deleteDept = async (deptId: string) => {
    try {
        const response = await apiClient.delete(`/api/v1.0/accounts/depts/${deptId}`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const updateDept = async (deptId: string, name: string, parentDeptId: string, leaderId: string, approverIdList: string[]) => {
    try {
        const response = await apiClient.patch(`/api/v1.0/accounts/depts/${deptId}`, {
            name,
            parent_dept_id: parentDeptId,
            leader_id: leaderId,
            approver_id_list: approverIdList
        });
        return response.data;
    } catch (error) {
        throw error;
    }
}
export const updateDeptParentDept = async (deptId: string, parentDeptId: string) => {
    try {
        const response = await apiClient.patch(`/api/v1.0/accounts/depts/${deptId}/parent_dept`, {
            parent_dept_id: parentDeptId,
        });
        return response.data;
    } catch (error) {
        throw error;
    }
}

export const getDeptDetail = async (deptId: string) => {
    try {
        const response = await apiClient.get(`/api/v1.0/accounts/depts/${deptId}`);
        return response.data;
    } catch (error) {
        throw error;
    }
}

export const getDeptPaths = async (search_value: string) => {
    try {
        const response = await apiClient.get(`/api/v1.0/accounts/dept_paths`, { params: { search_value: search_value } });
        return response.data;
    } catch (error) {
        throw error;
    }
}
export const getDeptPath = async (dept_id: string) => {
    try {
        const response = await apiClient.get(`/api/v1.0/accounts/dept_paths/${dept_id}`);
        return response.data;
    } catch (error) {
        throw error;
    }
}
