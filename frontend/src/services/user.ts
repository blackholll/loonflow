import { request } from 'umi';

export interface QueryUserSimpleType {
  search_value?: string;
}


export async function query() {
  return request<API.CurrentUser[]>('/api/users');
}

export async function queryCurrent() {
  return request<API.CurrentUser>('/api/currentUser');
}

export async function queryNotices(): Promise<any> {
  return request<{ data: API.NoticeIconData[] }>('/api/notices');
}

export async function queryUserSimple(params: QueryUserSimpleType) {
  return request<API.queryUserSimpleData>('/api/v1.0/simple_users', {
    method: 'get',
    params: params,
  })

}
