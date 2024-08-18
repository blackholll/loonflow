import axios from 'axios';
import * as API from './API';


const instance = axios.create({
    baseURL: '/api/v1.0',
  });
  
export async function AccountLogin(params: API.LoginParamsType) {
    const response = await instance.post('/login', params);
    console.log('response11:', response);
    return response.data;
}
