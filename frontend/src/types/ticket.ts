import { IApiResponse, IApiErrResponse, ISimpleEntity } from './common';
import { ISimpleUser } from './user';


export interface ITicketListQueryParam {
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
  transitionId: string;
  [propName: string]: any;
}

export interface IHandleTicketReqParam {
  transitionId: number;
  comment?: string;
  [propName: string]: any;
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
  creator: ISimpleUser;
  creatorDisplayName: string;
  createTime: string;
  updateTime: string;
}

export interface ITicketListResData {
  page: number;
  perPage: number;
  total: number;
  ticketList: ITicketListResEntity[]
}

export interface ITicketListRes extends IApiResponse<ITicketListResData> { }
