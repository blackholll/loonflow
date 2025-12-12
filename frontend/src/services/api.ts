import axios from 'axios';
import camelcaseKeys from 'camelcase-keys';
import snakecaseKeys from 'snakecase-keys';
import { getCookie, removeCookie } from '../utils/cookie';


const apiClient = axios.create({
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const token = getCookie('jwtToken');
    if (token && !config.url?.includes('/api/v1.0/login')) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    if (config.data && typeof config.data === 'object') {
      config.data = snakecaseKeys(config.data, { deep: true });
    }
    if (config.params && typeof config.params === 'object') {
      config.params = snakecaseKeys(config.params, { deep: true });
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);


apiClient.interceptors.response.use(
  (response) => {
    if (response.data && typeof response.data === 'object') {
      response.data = camelcaseKeys(response.data, { deep: true });
    }
    return response;
  },
  (error) => {

    if (error.response && error.response.status === 401) {
      removeCookie('jwtToken');
      window.location.href = '/signin';
    }

    return Promise.reject(error);
  }
);

export default apiClient;