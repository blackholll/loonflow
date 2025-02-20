import { IApiResponse } from './common';


export interface INotificationResEntity {
  id: string;
  label: string;
  created_at: string;
  updated_at: string;
  name: string;
  description: string;
  type: string;
  extra: any;
  tenant_id: string;
}

export interface INotificationListResData {
  application_info_list: INotificationResEntity[]
}

export interface INotificationListRes extends IApiResponse<INotificationListResData> {}