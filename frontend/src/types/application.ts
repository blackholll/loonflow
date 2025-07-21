import { IApiResponse } from './common';

// 定义 label 的类型为任意 key-value 对的字典对象
type LabelDict = Record<string, any>;

export interface IApplicationResEntity {
  id: string;
  label: LabelDict; // 修改为字典对象类型
  createdAt: string;
  updatedAt: string;
  name: string;
  description: string;
  type: string;
  token: string;
  tenantId: string;
}

export interface ISimpleApplicationResEntity {
  id: string;
  name: string;
  description: string;
  type: string;
  tenantId: string;
}
export interface IApplicationListResData {
  applicationInfoList: IApplicationResEntity[]
}

export interface ISimpleApplicationResData {
  applicationInfoList: ISimpleApplicationResEntity[]
}

export interface IApplicationListRes extends IApiResponse<IApplicationListResData> { }
export interface ISimpleApplicationListRes extends IApiResponse<ISimpleApplicationResData> { }
