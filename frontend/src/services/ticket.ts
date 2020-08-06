import { request } from 'umi';
// import request from 'umi-request'

export interface TicketParamsType {
  category: string;

}

export interface WorkflowParamsType {
  name?: string;

}


export async function getTicketList(params: TicketParamsType) {
  return request<API.TicketListData>('/api/v1.0/tickets', {
    method: 'get',
    params: params
  });
}

export async function getWorkflowList(params: WorkflowParamsType) {
  return request<API.WorkflowListData>('/api/v1.0/workflows', {
    method: 'get',
    params: params
  })
}

