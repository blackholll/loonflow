export interface IApiResponse<T> {
  code: 0;
  data: T;
  msg: string;
}

export interface IApiErrResponse {
  code: -1;
  msg: string;
}

export interface ISimpleUser {
  id: string,
  name: string,
  alias: string
}

export interface ISimpleEntity {
  id: string,
  name: string
}

export interface ISimpleQueryParam {
  page?: number;
  per_page?: number;
  search_key?: string

}