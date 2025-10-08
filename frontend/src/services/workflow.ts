
import apiClient from './api';
import { ISimpleWorkflowListRes, IWorkflowListRes, IWorkflowFullDefinitionRes, IWorkflowVersionListRes, IWorkflowReleaseRes, IWorkflowInitNodeRes } from '../types/workflow';
import { IApiErrResponse, } from '@/types/common';
import { IWorkflowActionsRes, IWorkflowCreationFormRes, IWorkflowDiagramRes } from '../types/workflow';





// export interface CommonSearchParamsType {
//   name?: string;
//   page?: number;
//   per_page?: number;
// }
// export interface WorkflowParamsType {
//   name?: string;
//   page?: number;
//   per_page?: number;
// }


// export interface CustomFiledParamsType {
//   search_value?: string;
//   page?: number;
//   per_page?: number;
// }

// export interface WorkflowInitStateParamsType {
//   workflowId: number
// }

// export interface  CustomFiledEditType {
//   field_key: string,
//   field_name: string,
//   field_type_id: number,
//   order_id: number,
//   label?: string,
//   description?: string,
//   field_template?: string,
//   default_value?: string,
//   boolean_field_display?: string,
//   field_choice?: string
// }

// export interface WorkflowStateParamsType {
//   search_value?: string;
//   page?: number;
//   per_page?: number;
// }
// export interface workflowStateEditType {
//   name: string,
//   order_id: number,
//   type_id: number,
//   is_hidden: number,
//   enable_retreat: number,
//   participant_type_id: number,
//   distribute_type_id: number,
//   remember_last_man_enable: number,
//   state_field_str: string,
//   label?: string,
// }


// export interface  WorkflowDetailType {
//   name: string,
//   description: string,
//   notices: string,
//   limit_expression: string,
//   display_form_str: string,
//   intervener: string,
//   api_permission_apps: string,
//   content_template: string,
//   title_template: string,
//   view_depts: string,
//   view_permission_check: boolean,
//   view_persons: string,
//   workflow_admin: string
// }

// export interface  workflowTransitionEditType {
//   name: string,
// }

// export interface  workflowStatisticsType {
//   time_start: string,
//   time_end: string,
// }


export const getSimpleWorkflowList = async (search_value: string, page: number, per_page: number): Promise<ISimpleWorkflowListRes | IApiErrResponse> => {
  try {
    const response = await apiClient.get('/api/v1.0/simple_workflows', { params: { search_value, page, per_page } });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getWorkflowList = async (search_value: string, page: number, per_page: number): Promise<IWorkflowListRes | IApiErrResponse> => {
  try {
    const response = await apiClient.get('/api/v1.0/workflows', { params: { search_value, page, per_page } });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getWorkflowDetail = async (workflowId: string, versionName?: string): Promise<IWorkflowFullDefinitionRes | IApiErrResponse> => {
  try {
    const response = await apiClient.get(`/api/v1.0/workflows/${workflowId}`, { params: { version_name: versionName } });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const addWorkflow = async (params: any): Promise<IWorkflowReleaseRes | IApiErrResponse> => {
  try {
    const response = await apiClient.post('/api/v1.0/workflows', params);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const updateWorkflow = async (workflowId: string, params: any): Promise<ISimpleWorkflowListRes | IApiErrResponse> => {
  try {
    const response = await apiClient.patch(`/api/v1.0/workflows/${workflowId}`, params);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const deleteWorkflow = async (workflowId: string): Promise<ISimpleWorkflowListRes | IApiErrResponse> => {
  try {
    const response = await apiClient.delete(`/api/v1.0/workflows/${workflowId}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getWorkflowVersionList = async (workflowId: string, searchValue: string, page: number, perPage: number): Promise<IWorkflowVersionListRes | IApiErrResponse> => {
  try {
    const response = await apiClient.get(`/api/v1.0/workflows/${workflowId}/versions`, { params: { searchValue, page, perPage } });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getTicketCreationForm = async (workflowId: string, versionName?: string): Promise<IWorkflowCreationFormRes | IApiErrResponse> => {
  try {
    const response = await apiClient.get(`/api/v1.0/workflows/${workflowId}/ticket_creation_form`, { params: { version_name: versionName } });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getTicketCreationActions = async (workflowId: string, versionName?: string): Promise<IWorkflowActionsRes | IApiErrResponse> => {
  try {
    const response = await apiClient.get(`/api/v1.0/workflows/${workflowId}/ticket_creation_actions`, { params: { version_name: versionName } });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getWorkflowDiagram = async (workflowId: string, versionId?: string): Promise<IWorkflowDiagramRes | IApiErrResponse> => {
  try {
    const response = await apiClient.get(`/api/v1.0/workflows/${workflowId}/process_single_schema`, { params: { version_id: versionId } });
    return response.data;
  } catch (error) {
    throw error;
  }
};


// export async function getWorkflowDetail(workflowId: Number) {
//   return request<API.CommonResponse>(`/api/v1.0/workflows/${workflowId}`, {
//     method: 'get'
//   })
// }

// export async function delWorkflow(workflowId: Number) {
//   return request<API.CommonResponse>(`/api/v1.0/workflows/${workflowId}`, {
//     method: 'delete'
//   })
// }

// export async function updateWorkflowDetail(workflowId: Number, params: WorkflowDetailType) {
//   return request<API.CommonResponse>(`/api/v1.0/workflows/${workflowId}`, {
//     method: 'patch',
//     data: params
//   })
// }


// export async function getWorkflowInitState(params: WorkflowInitStateParamsType) {
//   return request<API.WorkflowInitStateData>(`/api/v1.0/workflows/${params.workflowId}/init_state`, {
//     method: 'get',
//   })
// }

// export async function getWorkflowCustomField(workflowId: Number, params:CustomFiledParamsType) {
//   return request<API.WorkflowInitStateData>(`/api/v1.0/workflows/${workflowId}/custom_fields`, {
//     method: 'get',
//     params: params
//   })
// }

// export async function addCustomField(workflowId: Number, params: CustomFiledEditType) {
//   return request<API.CommonResponse> (`/api/v1.0/workflows/${workflowId}/custom_fields`, {
//     method: 'post',
//     data: params
//   })
// }

// export async function updateCustomField(workflowId: Number, customFieldId: Number, params:CustomFiledEditType) {
//   return request<API.CommonResponse> (`/api/v1.0/workflows/${workflowId}/custom_fields/${customFieldId}`, {
//     method: 'patch',
//     data: params
//   })
// }

// export async function delCustomField(workflowId: Number, customFieldId: Number) {
//   return request<API.CommonResponse> (`/api/v1.0/workflows/${workflowId}/custom_fields/${customFieldId}`,{
//     method: 'delete',
//   })
// }

// export async function getWorkflowState(workflowId: Number, params:WorkflowStateParamsType) {
//   return request<API.CommonResponse> (`/api/v1.0/workflows/${workflowId}/states`, {
//     method: 'get',
//     params: params
//   })
// }

// export async function getWorkflowSimpleState(workflowId: Number, params:WorkflowStateParamsType) {
//   return request<API.CommonResponse> (`/api/v1.0/workflows/${workflowId}/simple_states`, {
//     method: 'get',
//     params: params
//   })
// }

// export async function updateWorkflowState(workflowId: Number, stateId: Number, params:workflowStateEditType) {
//   return request<API.CommonResponse> (`/api/v1.0/workflows/${workflowId}/states/${stateId}`, {
//     method: 'patch',
//     data: params
//   })
// }

// export async function addWorkflow(params:WorkflowDetailType) {
//   return request<API.CommonResponse> (`/api/v1.0/workflows`, {
//     method: 'post',
//     data: params
//   })
// }

// export async function addWorkflowState(workflowId: Number, params:workflowStateEditType) {
//   return request<API.CommonResponse> (`/api/v1.0/workflows/${workflowId}/states`, {
//     method: 'post',
//     data: params
//   })
// }

// export async function addWorkflowTransition(workflowId: Number, params:workflowTransitionEditType) {
//   return request<API.CommonResponse> (`/api/v1.0/workflows/${workflowId}/transitions`, {
//     method: 'post',
//     data: params
//   })
// }

// export async function delWorkflowState(workflowId: Number, stateId: Number) {
//   return request<API.CommonResponse> (`/api/v1.0/workflows/${workflowId}/states/${stateId}`,{
//     method: 'delete',
//   })
// }


// export async function  getWorkflowTransition(workflowId: Number, params:CommonSearchParamsType) {
//   return request<API.CommonResponse>(`/api/v1.0/workflows/${workflowId}/transitions`, {
//     method: 'get',
//     params: params
//   })
// }
// export async function  updateWorkflowTransition(workflowId: Number, transitionId:Number, params:workflowTransitionEditType) {
//   return request<API.CommonResponse>(`/api/v1.0/workflows/${workflowId}/transitions/${transitionId}`, {
//     method: 'patch',
//     data: params
//   })
// }

// export async function delWorkflowTransition(workflowId:Number, transitionId:Number){
//   return request<API.CommonResponse>(`/api/v1.0/workflows/${workflowId}/transitions/${transitionId}`,{
//     method: 'delete'
//   })
// }

// export async function getWorkflowSimpleDescription(workflowId: Number){
//   return request<API.CommonResponse>(`/api/v1.0/workflows/${workflowId}/simple_description`, {
//     method: 'get'
//   })
// }

// export async function canInterveneRequest(workflowId: number) {
//   return request<API.CommonResponse> (`/api/v1.0/workflows/${workflowId}/can_intervene`, {
//     method: 'get',
//   })
// }


// export async function workflowStatisticsRequest(workflowId: number, params:workflowStatisticsType) {
//   return request<API.CommonResponse> (`/api/v1.0/workflows/${workflowId}/statistics`, {
//     method: 'get',
//     params: params
//   })
// }

