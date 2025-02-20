import apiClient from './api';


interface INotificationNew {
  name: string, 
  description: string,
  type: string, 
  extra: string
}

export const getNotificationList = async(searchValue: string, page: number, perPage:number) => {
  const response = await apiClient.get('/api/v1.0/manage/notifications', { params: { search_value: searchValue, page, per_page:perPage}});
  return response.data;
};

export const delNotification = async(notificationId:string) => {
  const response = await apiClient.delete(`/api/v1.0/manage/notifications/${notificationId}`);
  return response.data;
};
export const getNotificationDetail = async(notificationID: string) => {
  const response = await apiClient.get(`/api/v1.0/manage/notifications/${notificationID}`);
  return response.data
};

export const addNotification = async(params:INotificationNew) => {
  const response = await apiClient.post('/api/v1.0/manage/notifications', params);
  return response.data;
}

export const updateNotification = async(notification_id:string, params:INotificationNew) => {
  const response = await apiClient.patch(`/api/v1.0/manage/notifications/${notification_id}`, params);
  return response.data;
}