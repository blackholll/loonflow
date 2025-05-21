export interface IApiResponse<T> {
  code: 0;
  data: T;
  msg: string;
}

export interface IApiErrResponse {
  code: -1;
  msg: string;
}

export interface ISimpleEntity {
  id: string,
  name: string
}

export interface ISimpleQueryParam {
  page?: number;
  perPage?: number;
  searchKey?: string

}