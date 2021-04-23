import { request } from 'umi';

export interface CommonSearchType {
  search_value?: string;
  page?: number;
  per_page?: number
}

export interface QueryUserSimpleType {
  search_value?: string;
}

export interface GetUserListType {
  search_value?: string;
  page?: number;
  per_page?: number
}

export interface getUserRoleType {
  search_value?: string;
  page?: number;
  per_page?: number
}

export interface getRoleListType{
  search_value?: string,
  page?: number,
  per_page?: number
}

export interface getCommonListType {
  search_value?: string,
  page?: number,
  per_page?: number
}


export interface addRoleUserType {
  user_id: number
}

export interface updateRoleType {
  name: string,
  description?: string,
  label?: string
}

export interface addDeptType {
  name: string,
  parent_dept_id?: number,
  leader?: string,
  approver?: string,
  label?: string
}

export interface TokenType {
  app_name: string,
  ticket_sn_prefix?: string
}

export interface passwordType {
  source_password: string,
  new_password: string,
  new_password_again: string

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
  return request<API.queryUserSimpleData>('/api/v1.0/accounts/simple_users', {
    method: 'get',
    params: params,
  })
}

export async function getUserList(params: GetUserListType) {
  return request<API.CommonResponse>('/api/v1.0/accounts/users', {
    method: 'get',
    params: params
  })
}

export async function getDeptList(params: GetDeptListType) {
  return request<API.CommonResponse> ('/api/v1.0/accounts/depts',{
    method: 'get',
    params: params
  })
}

export async function getSimpleDeptList(params: GetUserListType) {
  return request<API.CommonResponse> ('/api/v1.0/accounts/simple_depts',{
    method: 'get',
    params: params
  })
}

export async function addUser(params: AddUserType) {
  return request<API.CommonResponse> ('/api/v1.0/accounts/users', {
    method: 'post',
    data: params
  })
}

export async function updateUser(userId: number, params: UpdateUserType ){
  return request<API.CommonResponse> (`/api/v1.0/accounts/users/${userId}`,{
    method: 'patch',
    data: params
  })
}

export async function delUserRequest(userId: number){
  return request<API.CommonResponse> (`/api/v1.0/accounts/users/${userId}`,{
    method: 'delete',
  })
}
export async function delRoleRequest(roleId: number){
  return request<API.CommonResponse> (`/api/v1.0/accounts/roles/${roleId}`,{
    method: 'delete',
  })
}

export async function getUserRole(userId: number, params: getUserRoleType) {
  return request<API.CommonResponse> (`/api/v1.0/accounts/users/${userId}/roles`)

}

export async function resetUserPasswd(userId: number) {
  return request<API.CommonResponse> (`/api/v1.0/accounts/users/${userId}/reset_password`, {
    method: 'post'
  })
}

export async function getRoleList(params: getRoleListType) {
  return request<API.CommonResponse> ('/api/v1.0/accounts/roles', {
    method: 'get',
    params: params
  })
}

export async function addRole(params: updateRoleType) {
  return request<API.CommonResponse> ('/api/v1.0/accounts/roles', {
    method: 'post',
    data: params
  })
}

export async function updateRole(roleId: number, params: updateRoleType) {
  return request<API.CommonResponse> (`/api/v1.0/accounts/roles/${roleId}`, {
    method: 'patch',
    data: params
  })
}

export async function getRoleUserList(roleId: number, params: getCommonListType) {
  return request<API.CommonResponse> (`/api/v1.0/accounts/roles/${roleId}/users`, {
    method: 'get',
    params: params
  })
}

export async function addRoleUser(roleId: number, params: addRoleUserType) {
  return request<API.CommonResponse>(`/api/v1.0/accounts/roles/${roleId}/users`, {
    method: 'post',
    data: params
  })
}

export async function delRoleUserRequest(roleId: number, userId: number) {
  return request<API.CommonResponse>(`/api/v1.0/accounts/roles/${roleId}/users/${userId}`, {
    method: 'delete',
  })
}

export async function delDeptRequest(deptId: number) {
  return request<API.CommonResponse> (`/api/v1.0/accounts/depts/${deptId}`, {
    method: 'delete',
  })
}

export async function addDeptRequest(params: addDeptType) {
  return request<API.CommonResponse> ('/api/v1.0/accounts/depts', {
    method: 'post',
    data: params
  })
}

export async function updateDeptRequest(deptId: number, params: addDeptType) {
  return request<API.CommonResponse> (`/api/v1.0/accounts/depts/${deptId}`, {
    method: 'patch',
    data: params
  })
}

export async function getTokenListRequest(params: CommonSearchType) {
  return request<API.CommonResponse> ('/api/v1.0/accounts/app_token', {
    method: 'get',
    params: params
  })
}
export async function getSimpleTokenListRequest(params: CommonSearchType) {
  return request<API.CommonResponse> ('/api/v1.0/accounts/simple_app_token', {
    method: 'get',
    params: params
  })
}

export async function addTokenRequest(params: TokenType) {
  return request<API.CommonResponse> ('/api/v1.0/accounts/app_token', {
    method: 'post',
    data: params
  })
}

export async function updateTokenRequest(tokenId: number, params: tokenType){
  return request<API.CommonResponse> (`/api/v1.0/accounts/app_token/${tokenId}`, {
    method: 'patch',
    data: params
  })
}

export async function delTokenRequest(tokenId: number) {
  return request<API.CommonResponse> (`/api/v1.0/accounts/app_token/${tokenId}`, {
    method: 'delete',
  })
}


export async function changeUserPassword(params: passwordType) {
  return request<API.CommonResponse> (`/api/v1.0/accounts/users/change_password`, {
    method: 'post',
    data: params
  })
}
