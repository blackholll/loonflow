import { request } from 'umi';
// import request from 'umi-request'

export interface TicketParamsType {
  category: string;
  [propName: string]: any;
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

export interface changeStateParamsType {
  state_id: number;
  suggestion?: string;
}

export interface deliverTicketParamsType {
  target_username: string;
  suggestion?: string;
}

export interface addNodeTicketParamsType {
  target_username: string;
  suggestion?: string;
}

export interface closeTicketParamsType {
  suggestion?: string;
}

export interface commentTicketParamsType {
  suggestion: string;
}

export interface delTicketParamsType {
  suggestion: string;
}

export interface retreatTicketParamsType {
  suggestion: string;
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

export async function getTicketFlowLogRequest(ticketId: number) {
  return request<API.CommonResponse> (`/api/v1.0/tickets/${ticketId}/flowlogs`,{
    method: 'get',
  })
}


export async function getTicketStepRequest(ticketId: number) {
  return request<API.CommonResponse> (`/api/v1.0/tickets/${ticketId}/flowsteps`,{
    method: 'get',
  })
}

export async function closeTicketRequest(ticketId: number, params:closeTicketParamsType) {
  return request<API.CommonResponse> (`/api/v1.0/tickets/${ticketId}/close`,{
    method: 'post',
    data: params
  })
}

export async function deliverTicketRequest(ticketId: number, params:deliverTicketParamsType) {
  return request<API.CommonResponse> (`/api/v1.0/tickets/${ticketId}/deliver`,{
    method: 'post',
    data: params
  })
}

export async function addNodeTicketRequest(ticketId: number, params:addNodeTicketParamsType) {
  return request<API.CommonResponse> (`/api/v1.0/tickets/${ticketId}/add_node`,{
    method: 'post',
    data: params
  })
}

export async function addNodeEndTicketRequest(ticketId: number, params:addNodeTicketParamsType) {
  return request<API.CommonResponse> (`/api/v1.0/tickets/${ticketId}/add_node_end`,{
    method: 'post',
    data: params
  })
}

export async function changeTicketStateRequest(ticketId: number, params:changeStateParamsType) {
  return request<API.CommonResponse> (`/api/v1.0/tickets/${ticketId}/state`, {
    method: 'put',
    data: params
  })
}

export async function acceptTicketRequest(ticketId: number) {
  return request<API.CommonResponse> (`/api/v1.0/tickets/${ticketId}/accept`, {
    method: 'post',
  })
}

export async function addCommentRequest(ticketId: number, params:commentTicketParamsType) {
  return request<API.CommonResponse> (`/api/v1.0/tickets/${ticketId}/comments`, {
    method: 'post',
    data: params
  })
}


export async function delTicketRequest(ticketId: number, params:delTicketParamsType) {
  return request<API.CommonResponse> (`/api/v1.0/tickets/${ticketId}`, {
    method: 'delete',
    data: params
  })
}

export async function retreatRequest(ticketId: number, params:retreatTicketParamsType) {
  return request<API.CommonResponse> (`/api/v1.0/tickets/${ticketId}/retreat`, {
    method: 'post',
    data: params
  })
}
