import axios, { type AxiosError, type AxiosResponse } from 'axios';
import { LocalRecommendationEngine } from './LocalRecommendationEngine';

export interface ApiResponse<T> {
  status: 'success' | 'error';
  data?: T;
  message?: string;
}

const resolveApiBaseUrl = (): string => {
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }

  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname;
    if (hostname === '10.0.2.2') {
      return 'http://10.0.2.2:8001/api/v1';
    }
    if (hostname) {
      return `http://${hostname}:8001/api/v1`;
    }
  }

  return 'http://localhost:8001/api/v1';
};

const apiClient = axios.create({
  baseURL: resolveApiBaseUrl(),
  timeout: 2500,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error: AxiosError) => {
    if (!error.response || error.code === 'ECONNABORTED') {
      const config = error.config;
      if (config && config.url && config.url.includes('/chat')) {
        let intent = { query: '' };
        if (config.data) {
          try {
            intent = typeof config.data === 'string' ? JSON.parse(config.data) : config.data;
          } catch (e) {}
        }
        const offlineResult = LocalRecommendationEngine.getRecommendations(intent);
        
        return Promise.resolve({
          data: {
             status: 'success',
             data: offlineResult,
             message: 'Offline fallback'
          },
          status: 200,
          statusText: 'OK',
          headers: {},
          config: config,
        } as AxiosResponse);
      }
    }
    
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default apiClient;
