import { request } from 'umi';

export interface NoticeListRequestParamsType {
  per_page?: number,
  page?: number
}

export interface addNoticeListRequestParamsType {
  name: string,
  description: string,
  type_id: number,
  hook_url?: string;
  hook_token?: string;
  corpid?: string;
  corpsecret?: string;
  appkey?: string;
  appsecret?: string;
}

export interface getNoticeDetailRequestParamsType {
  noticeId: number
}

export interface delNoticeDetailRequestParamsType {
  noticeId: number
}

export interface updateNoticeDetailRequestParamsType {
  noticeId: number,
  name: string
  description: string
  type_id: number,
  hook_url?: string,
  hook_token?: string,
  corpid?: string,
  corpsecret?: string,
  appkey?: string,
  appsecret?: string,
}


export async function getNoticeListRequest(params: NoticeListRequestParamsType) {
  return request<API.TicketListData>('/api/v1.0/workflows/custom_notices', {
    method: 'get',
    params: params
  });
}

export async function getSimpleNoticeListRequest(params: NoticeListRequestParamsType) {
  return request<API.TicketListData>('/api/v1.0/workflows/simple_custom_notices', {
    method: 'get',
    params: params
  });
}

export async function addNoticeListRequest(params: addNoticeListRequestParamsType) {
  return request<API.CommonResponse>('/api/v1.0/workflows/custom_notices', {
    method: 'post',
    data: params,
  })
}

export async function getNoticeDetailRequest(params: getNoticeDetailRequestParamsType) {
  return request<API.CommonResponse>(`/api/v1.0/workflows/custom_notices/${params.noticeId}`, {
    method: 'get',
  })
}

export async function delNoticeDetailRequest(params: delNoticeDetailRequestParamsType) {
  return request<API.CommonResponse>(`/api/v1.0/workflows/custom_notices/${params.noticeId}`, {
    method: 'delete',
  })
}


export async function updateNoticeDetailRequest(noticeId: number, params: updateNoticeDetailRequestParamsType) {
  console.log(`updatenoteic: ${noticeId}`);
  return request<API.CommonResponse>(`/api/v1.0/workflows/custom_notices/${noticeId}`, {
    method: 'patch',
    data: params
  })
}
