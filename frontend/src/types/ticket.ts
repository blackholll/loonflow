import { IApiResponse, ISimpleEntity } from './common';
import { ISimpleUser } from './user';
import { IWorkflowAction, IFormSchema } from './workflow';


export interface ITicketListQueryParam {
  searchKey?: string;
  page: number;
  perPage: number;
  category: string;
  parentTicketId?: string;
  [propName: string]: any;
}

export interface IWorkflowListQueryParam {
  searchKey?: string;
}

export interface INewTicketReqParam {
  workflowId: string;
  actionId: string;
  fields: any;
}

export interface IActionProps {
  nodeId?: string;
  targetAssigneeId?: string;
  comment?: string;
}

export interface IHandleTicketReqParam {
  ticketId: string;
  actionType: string;
  actionId: string;
  comment?: string;
  fields?: any;
  actionProps?: IActionProps;
}

export interface ITicketDetailReqParam {
  ticketId: string;
}

export interface IChangeTicketNodeParam {
  nodeId: string;
  comment?: string;
}

export interface IDeliverTicketParam {
  targetUesrname: string;
  comment?: string;
}

export interface IAddNodeTicketParam {
  targetUsername: string;
  comment?: string;
}

export interface ICloseTicketParam {
  comment?: string;
}

export interface ICommentTicketParam {
  commment: string;
}

export interface IDelTicketParam {
  commment: string;
}

export interface IRetreatTicketParam {
  comment: string;
}


export interface ITicketListResEntity {
  id: number;
  title: string;
  node: ISimpleEntity,
  workflow: ISimpleEntity;
  creatorInfo: ISimpleUser;
  actState: string
  createdAt: string;
  updatedAt: string;
}

export interface ITicketListResData {
  page: number;
  perPage: number;
  total: number;
  ticketList: ITicketListResEntity[]
}
export interface INewTicketResData {
  ticketId: string;
}

export interface ITicketListRes extends IApiResponse<ITicketListResData> { }

export interface INewTicketRes extends IApiResponse<INewTicketResData> { }


export interface ITicketActionsRes extends IApiResponse<{ actions: IWorkflowAction, actionBaseNodeId: string }> { }

export interface ITicketDetailFormRes extends IApiResponse<{ formSchema: IFormSchema }> { }

export interface IHandleTicketRes extends IApiResponse<{ ticketId: string }> { }

// flowlogs
export interface ITicketFlowHistoryItem {
  id: string;
  processorInfo: ITicketProcessorInfo;
  createdAt: string; // ISO string
  actionName: string;
  actionType: string;
  comment: string;
}

export interface ITicketProcessorInfo {
  processorAlias: string;
  processorEmail: string;
  processorPhone: string;
  processorType: string;
  processor: string;
}
export interface ITicketFlowHistoryResData {
  page: number;
  perPage: number;
  total: number;
  value: ITicketFlowHistoryItem[];
}

export interface ITicketFlowHistoryRes extends IApiResponse<ITicketFlowHistoryResData> { }

export interface ITicketCurrentNodeInfoItem {
  id: string;
  name: string;
}
export interface ITicketCurrentNodeInfosRes extends IApiResponse<{ currentNodeInfoList: ITicketCurrentNodeInfoItem[] }> { }