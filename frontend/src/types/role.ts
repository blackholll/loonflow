import { IApiResponse } from "./common";

export interface IRoleResEntity {
    id: string;
    label: string;
    createdAt: string;
    updatedAt: string;
    name: string;
    description: string;
    tenantId: string;
}

export interface ISimpleRole {
    id: string;
    name: string;
}

export interface IRoleListResData {
    roleList: IRoleResEntity[]
}

export interface IRoleListRes extends IApiResponse<IRoleListResData> { }