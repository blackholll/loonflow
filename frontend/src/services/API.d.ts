declare namespace API {
  export interface CurrentUser {
    id: number;
    username: string;
    phone: string;
    is_active: boolean;
    type_id: number;
    email: string;
  }

  export interface CommonResponse {
    code: number;
    data: any;
    msg: string;
  }

  export interface LoginStateType {
    code?: number;
    data?: any;
    type?: string;
  }

  export interface NoticeIconData {
    id: string;
    key: string;
    avatar: string;
    title: string;
    datetime: string;
    type: string;
    read?: boolean;
    description: string;
    clickClose?: boolean;
    extra: any;
    status: string;
  }

  export interface TicketListData {
    code: number;
    data: any;
    msg: string;
  }

  export interface WorkflowListData {
    code: number;
    data: any;
    msg: string;
  }

  export interface WorkflowInitStateData {
    code: number;
    data: any;
    msg: string;
  }

  export interface queryUserSimpleData {
    code: number;
    data: any;
    msg: string;
  }



}


