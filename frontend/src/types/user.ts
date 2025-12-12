import { IApiResponse } from './common';

export interface IUser {
    id: string;
    name: string;
    type: string;
    alias: string;
    email: string;
    tenantId: string;
    phone: string;
    avatar?: string;
    lang?: string;
    isActive: boolean;
    deptInfoList: any[]; // 使用any避免循环依赖，实际使用时应该导入ISimpleDept
}

export interface IUserListResData {
    page: number;
    perPage: number;
    total: number;
    userInfoList: IUser[]
}

export interface IUserSimpleListResData {
    page: number;
    perPage: number;
    total: number;
    userInfoList: ISimpleUser[]
}

export interface ISimpleUser {
    id: string;
    name: string;
    alias: string;
    email: string;
}

export interface ISimpleUserListRes extends IApiResponse<IUserSimpleListResData> { }
