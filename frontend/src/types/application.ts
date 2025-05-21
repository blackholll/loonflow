import { IApiResponse } from './common';


export interface IApplicationResEntity {
  id: string;
  label: string;
  createdAt: string;
  updatedAt: string;
  name: string;
  description: string;
  type: string;
  token: string;
  tenantId: string;
}

export interface IApplicationListResData {
  applicationInfoList: IApplicationResEntity[]
}

export interface IApplicationListRes extends IApiResponse<IApplicationListResData> { }