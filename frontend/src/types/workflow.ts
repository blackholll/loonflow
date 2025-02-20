import { IApiResponse } from '../types/common';



export interface ISimpleWorkflowEntity {
  id: string,
  name: string,
  description: string
}

export interface ISimpleWorkflowListResData {
  page: number;
  per_page: number;
  total: number;
  workflow_info_list: ISimpleWorkflowEntity[]
}

export interface ISimpleWorkflowListRes extends IApiResponse<ISimpleWorkflowListResData> {}
