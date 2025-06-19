import { IApiResponse } from '../types/common';



export interface ISimpleWorkflowEntity {
  id: string,
  name: string,
  description: string
}
export interface IWorkflowEntity {
  id: string,
  name: string,
  description: string,
  createdAt: string,
  updatedAt: string,
  creator: string,
}

export interface ISimpleWorkflowListResData {
  page: number;
  perPage: number;
  total: number;
  workflowInfoList: ISimpleWorkflowEntity[]
}

export interface IWorkflowListResData {
  page: number;
  perPage: number;
  total: number;
  workflowInfoList: IWorkflowEntity[]
}

export interface IWorkflowDetailInfo {
  basicInfo: {
    name: string,
    description: string
  }
  noticeInfo: {
    title: string,
    content: string
  }
  fieldInfoList: []
}

export interface ISimpleWorkflowListRes extends IApiResponse<ISimpleWorkflowListResData> { }

export interface IWorkflowListRes extends IApiResponse<IWorkflowListResData> { }
