import { IApiResponse } from './common';


export interface ITenantDetailResEntity {
  id: string;
  label: string;
  created_at: string;
  updated_at: string;
  name: string;
  domain: string;
  icon: string;
  workflow_limit: number;
  ticket_limit: number;
}

export interface ITenantBasicInfo {
  id: string;
  name: string;
  domain: string;
  icon: string
}

export interface ITenantDetailResData {
  tenant_info: ITenantDetailResEntity
}

export interface ITenantBasicInfoResData {
  tenant_info: ITenantBasicInfo
}


export interface ITenantDetailRes extends IApiResponse<ITenantDetailResData> {}

export interface ITenantBasicInfoRes extends IApiResponse<ITenantBasicInfoResData> {}