import { request } from 'umi';

export interface WorkflowParamsType {
  name?: string;
  page?: number;
  per_page?: number;
}

export interface CustomFiledParamsType {
  search_value?: string;
  page?: number;
  per_page?: number;
}

export interface WorkflowInitStateParamsType {
  workflowId: number
}

export interface  CustomFiledEditType {
  field_key: string,
  field_name: string,
  field_type_id: number,
  order_id: number,
  label?: string,
  description?: string,
  field_template?: string,
  default_value?: string,
  boolean_field_display?: string,
  field_choice?: string
}

export interface WorkflowStateParamsType {
  search_value?: string;
  page?: number;
  per_page?: number;
}
export interface workflowStateEditType {
  name: string,
  order_id: number,
  type_id: number,
  is_hidden: number,
  enable_retreat: number,
  participant_type_id: number,
  distribute_type_id: number,
  remember_last_man_enable: number,
  state_field_str: string,
  label?: string,

}

export async function getWorkflowList(params: WorkflowParamsType) {
  return request<API.WorkflowListData>('/api/v1.0/workflows', {
    method: 'get',
    params: params
  })
}

export async function getWorkflowDetail(workflowId: Number) {
  return request<API.CommonResponse>(`/api/v1.0/workflows/${workflowId}`, {
    method: 'get'
  })
}

export async function getWorkflowInitState(params: WorkflowInitStateParamsType) {
  return request<API.WorkflowInitStateData>(`/api/v1.0/workflows/${params.workflowId}/init_state`, {
    method: 'get',
  })
}

export async function getWorkflowCustomField(workflowId: Number, params:CustomFiledParamsType) {
  return request<API.WorkflowInitStateData>(`/api/v1.0/workflows/${workflowId}/custom_fields`, {
    method: 'get',
    params: params
  })
}

export async function addCustomField(workflowId: Number, params: CustomFiledEditType) {
  return request<API.CommonResponse> (`/api/v1.0/workflows/${workflowId}/custom_fields`, {
    method: 'post',
    data: params
  })
}

export async function updateCustomField(workflowId: Number, customFieldId: Number, params:CustomFiledEditType) {
  return request<API.CommonResponse> (`/api/v1.0/workflows/${workflowId}/custom_fields/${customFieldId}`, {
    method: 'patch',
    data: params
  })
}

export async function delCustomField(workflowId: Number, customFieldId: Number) {
  return request<API.CommonResponse> (`/api/v1.0/workflows/${workflowId}/custom_fields/${customFieldId}`,{
    method: 'delete',
  })
}

export async function getWorkflowState(workflowId: Number, params:WorkflowStateParamsType) {
  return request<API.CommonResponse> (`/api/v1.0/workflows/${workflowId}/states`, {
    method: 'get',
    params: params
  })
}

export async function updateWorkflowState(workflowId: Number, stateId: Number, params:workflowStateEditType) {
  return request<API.CommonResponse> (`/api/v1.0/workflows/${workflowId}/states/${stateId}`, {
    method: 'patch',
    data: params
  })
}

export async function addWorkflowState(workflowId: Number, params:workflowStateEditType) {
  return request<API.CommonResponse> (`/api/v1.0/workflows/${workflowId}/states`, {
    method: 'post',
    data: params
  })
}

export async function delWorkflowState(workflowId: Number, stateId: Number) {
  return request<API.CommonResponse> (`/api/v1.0/workflows/${workflowId}/states/${stateId}`,{
    method: 'delete',
  })
}


