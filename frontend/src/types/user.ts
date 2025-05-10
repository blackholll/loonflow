import { IApiResponse } from './common';
import { ISimpleDept } from './dept';

export interface IUser {
    id: string;
    name: string;
    alias: string;
    email: string;
    tenant_id: string;
    phone: string;
    avatar: string;
    lang: string;
    status: string;
    dept_info_list: ISimpleDept[];
}

export interface IUserListResData {
    page: number;
    per_page: number;
    total: number;
    user_info_list: IUser[]
}

export interface ISimpleUser {
    id: string;
    name: string;
    alias: string;
    email: string;
}

export interface ISimpleUserListRes extends IApiResponse<IUserListResData> { }
