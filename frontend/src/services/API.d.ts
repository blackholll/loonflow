export interface LoginParamsType {
    email: string;
    password: string;
    mobile: string;
    captcha: string;
    type: string;
  }

export interface SimpleWorkflowListType {
    searchValue?: string;
    page?: number;
    perPage?: number;
}
