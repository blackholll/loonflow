import { IApiResponse } from './common';


export interface IApplicationResEntity {
  id: string;
  label: string;
  created_at: string;
  updated_at: string;
  name: string;
  description: string;
  type: string;
  token: string;
  tenant_id: string;
}

export interface IApplicationListResData {
  application_info_list: IApplicationResEntity[]
}

export interface IApplicationListRes extends IApiResponse<IApplicationListResData> {}