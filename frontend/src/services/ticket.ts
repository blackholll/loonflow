import { request } from 'umi';
// import request from 'umi-request'

export interface TicketParamsType {
  category: string;

}

export interface WorkflowParamsType {
  name?: string;
}

export interface  newTicketRequestParamsType {
  workflow_id: number;
  transition_id: number;
  suggestion?: string;
  [propName: string]: any;
}

export interface  handleTicketRequestParamsType {
  transition_id: number;
  suggestion?: string;
  [propName: string]: any;
}

export interface getDetailDetailRequestType {
  ticket_id: number;

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

export async function newTicketRequest(params: newTicketRequestParamsType) {
  return request<API.CommonResponse> ('/api/v1.0/tickets', {
    method: 'post',
    data: params
  })
}

export async function handleTicketRequest(ticketId: number, params: handleTicketRequestParamsType) {
  return request<API.CommonResponse> (`/api/v1.0/tickets/${ticketId}`, {
    method: 'patch',
    data: params
  })
}


export async function getDetailDetailRequest(params: getDetailDetailRequestType) {
  return request<API.CommonResponse> (`/api/v1.0/tickets/${params.ticket_id}`,{
    method: 'get',
  })
}

export async function getTicketTransitionRequest(params: getDetailDetailRequestType) {
  return request<API.CommonResponse> (`/api/v1.0/tickets/${params.ticket_id}/transitions`,{
    method: 'get',
  })
}
