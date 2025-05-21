import { IApiResponse } from './common';


export interface INotificationResEntity {
  id: string;
  label: string;
  createdAt: string;
  updatedAt: string;
  name: string;
  description: string;
  type: string;
  extra: any;
  tenantId: string;
}

export interface INotificationListResData {
  applicationInfoList: INotificationResEntity[]
}

export interface INotificationListRes extends IApiResponse<INotificationListResData> { }