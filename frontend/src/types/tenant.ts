import { IApiResponse } from './common';


export interface ITenantDetailResEntity {
  id: string;
  label: string;
  createdAt: string;
  updatedAt: string;
  name: string;
  domain: string;
  icon: string;
  workflowLimit: number;
  ticketLimit: number;
}

export interface ITenantBasicInfo {
  id: string;
  name: string;
  domain: string;
  icon: string
}

export interface ITenantDetailResData {
  tenantInfo: ITenantDetailResEntity
}

export interface ITenantBasicInfoResData {
  tenantInfo: ITenantBasicInfo
}


export interface ITenantDetailRes extends IApiResponse<ITenantDetailResData> { }

export interface ITenantBasicInfoRes extends IApiResponse<ITenantBasicInfoResData> { }