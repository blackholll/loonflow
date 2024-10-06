import axios from 'axios';
import { getCookie, removeCookie } from '../utils/cookie';


const apiClient = axios.create({
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const token = getCookie('jwtToken');
    // todo: jwt expire validation
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);


apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      removeCookie('jwtToken');
      window.location.href = '/signin';
    }
    return Promise.reject(error);
  }
);

export default apiClient;