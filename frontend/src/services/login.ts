import axios from 'axios';

export interface LoginParamsType {
  email: string;
  password: string;
  mobile: string;
  captcha: string;
  type: string;
}


const instance = axios.create({
    baseURL: '/api/v1.0',
  });
  
export async function AccountLogin(params: LoginParamsType) {
    const response = await instance.post('/login', params);
    console.log('response11:', response);
    return response.data;
}
