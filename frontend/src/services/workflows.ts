import { request } from 'umi';

export interface WorkflowParamsType {
  name?: string;
  page?: number;
  per_page?: number;
}

export interface WorkflowInitStateParamsType {
  workflowId: number
}

export async function getWorkflowList(params: WorkflowParamsType) {
  return request<API.WorkflowListData>('/api/v1.0/workflows', {
    method: 'get',
    params: params
  })
}

export async function getWorkflowInitState(params: WorkflowInitStateParamsType) {
  return request<API.WorkflowInitStateData>(`/api/v1.0/workflows/${params.workflowId}/init_state`, {
    method: 'get',
  })
}

