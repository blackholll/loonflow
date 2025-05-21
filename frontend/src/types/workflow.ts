import { IApiResponse } from '../types/common';



export interface ISimpleWorkflowEntity {
  id: string,
  name: string,
  description: string
}

export interface ISimpleWorkflowListResData {
  page: number;
  perPage: number;
  total: number;
  workflowInfoList: ISimpleWorkflowEntity[]
}

export interface ISimpleWorkflowListRes extends IApiResponse<ISimpleWorkflowListResData> { }
