
import apiClient from './api';
import { ITicketListRes, ITicketListQueryParam, ICommentTicketParam, IDelTicketParam, INewTicketReqParam, INewTicketRes, ITicketFlowHistoryRes } from '../types/ticket';
import { IApiErrResponse } from '@/types/common';
import { ITicketDetailFormRes, ITicketActionsRes, IHandleTicketReqParam, IHandleTicketRes } from '../types/ticket';


export const getTicketList = async (params: ITicketListQueryParam): Promise<ITicketListRes | IApiErrResponse> => {
  try {
    const response = await apiClient.get('/api/v1.0/tickets', {
      params: {
        'page': params.page,
        'per_page': params.perPage,
        'category': params.category,
        'parent_ticket_id': params.parentTicketId
      }
    }
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const newTicket = async (params: INewTicketReqParam): Promise<INewTicketRes | IApiErrResponse> => {
  const response = await apiClient.post('/api/v1.0/tickets', params);
  return response.data;
}

export const getTicketDetailForm = async (ticketId: string): Promise<ITicketDetailFormRes | IApiErrResponse> => {
  const response = await apiClient.get(`/api/v1.0/tickets/${ticketId}/ticket_detail_form`, { params: {} });
  return response.data;
};

export const getTicketDetailActions = async (ticketId: string): Promise<ITicketActionsRes | IApiErrResponse> => {
  const response = await apiClient.get(`/api/v1.0/tickets/${ticketId}/ticket_detail_actions`, { params: {} });
  return response.data;
};

export const handleTicket = async (params: IHandleTicketReqParam): Promise<IHandleTicketRes | IApiErrResponse> => {
  const response = await apiClient.post(`/api/v1.0/tickets/${params.ticketId}/handle`,
    { action_type: params.actionType, action_id: params.actionId, fields: params.fields, action_props: params.actionProps });
  return response.data;
};

export const getTicketFlowHistory = async (ticketId: string): Promise<ITicketFlowHistoryRes | IApiErrResponse> => {
  const response = await apiClient.get(`/api/v1.0/tickets/${ticketId}/ticket_flow_history`, { params: { desc: 0 } });
  return response.data;
}

// export const getWorkflowList = async (params: IWorkflowParam) => {
//   try {
//     const response = await apiClient.get('/api/v1.0/workflows', { params });
//     return response.data;
//   } catch (error) {
//     throw error;
//   }
// };

// export const newTicketRequest = async (params: INewTicketRequestParam) => {
//   try {
//     const response = await apiClient.post('/api/v1.0/tickets', params);
//     return response.data;
//   } catch (error) {
//     throw error;
//   }
// };

// export const handleTicketRequest = async (ticketId: number, params: IHandleTicketRequestParam) => {
//   try {
//     const response = await apiClient.patch(`/api/v1.0/tickets/${ticketId}`, params);
//     return response.data;
//   } catch (error) {
//     throw error;
//   }
// };

// export const getDetailRequest = async (params: IGetDetailRequest) => {
//   try {
//     const response = await apiClient.get(`/api/v1.0/tickets/${params.ticket_id}`);
//     return response.data;
//   } catch (error) {
//     throw error;
//   }
// };

// export const getTicketTransitionRequest = async (params: IGetDetailRequest) => {
//   try {
//     const response = await apiClient.get(`/api/v1.0/tickets/${params.ticket_id}/transitions`);
//     return response.data;
//   } catch (error) {
//     throw error;
//   }
// };

// export const getTicketFlowLogRequest = async (ticketId: number) => {
//   try {
//     const response = await apiClient.get(`/api/v1.0/tickets/${ticketId}/flowlogs`);
//     return response.data;
//   } catch (error) {
//     throw error;
//   }
// };

// export const getTicketStepRequest = async (ticketId: number) => {
//   try {
//     const response = await apiClient.get(`/api/v1.0/tickets/${ticketId}/flowsteps`);
//     return response.data;
//   } catch (error) {
//     throw error;
//   }
// };

// export const closeTicketRequest = async (ticketId: number, params: ICloseTicketParam) => {
//   try {
//     const response = await apiClient.post(`/api/v1.0/tickets/${ticketId}/close`, params);
//     return response.data;
//   } catch (error) {
//     throw error;
//   }
// };

// export const deliverTicketRequest = async (ticketId: number, params: IDeliverTicketParam) => {
//   try {
//     const response = await apiClient.post(`/api/v1.0/tickets/${ticketId}/deliver`, params);
//     return response.data;
//   } catch (error) {
//     throw error;
//   }
// };

// export const addNodeTicketRequest = async (ticketId: number, params: IAddNodeTicketParam) => {
//   try {
//     const response = await apiClient.post(`/api/v1.0/tickets/${ticketId}/add_node`, params);
//     return response.data;
//   } catch (error) {
//     throw error;
//   }
// };

// export const changeTicketStateRequest = async (ticketId: number, params: IChangeStateParam) => {
//   try {
//     const response = await apiClient.put(`/api/v1.0/tickets/${ticketId}/state`, params);
//     return response.data;
//   } catch (error) {
//     throw error;
//   }
// };

// export const acceptTicketRequest = async (ticketId: number) => {
//   try {
//     const response = await apiClient.post(`/api/v1.0/tickets/${ticketId}/accept`);
//     return response.data;
//   } catch (error) {
//     throw error;
//   }
// };

export const addCommentRequest = async (ticketId: number, params: ICommentTicketParam) => {
  try {
    const response = await apiClient.post(`/api/v1.0/tickets/${ticketId}/comments`, params);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const delTicketRequest = async (ticketId: number, params: IDelTicketParam) => {
  try {
    const response = await apiClient.delete(`/api/v1.0/tickets/${ticketId}`, { data: params });
    return response.data;
  } catch (error) {
    throw error;
  }
};

// export const retreatRequest = async (ticketId: number, params: IRetreatTicketParam) => {
//   try {
//     const response = await apiClient.post(`/api/v1.0/tickets/${ticketId}/retreat`, params);
//     return response.data;
//   } catch (error) {
//     throw error;
//   }
// };
