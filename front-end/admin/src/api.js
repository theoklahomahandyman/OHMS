import { ACCESS_TOKEN } from './constants';
import Cookies from 'js-cookie';
import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL
});

api.interceptors.request.use(
    (config) => {
        const token = Cookies.get(ACCESS_TOKEN);
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

const checkHealth = async (retries = 6, delay = 1000) => {
    try {
        const response = await api.get('/health/check/');
        if (response.data.status === 'ready') {
            return true;
        }
        throw new Error('Back-End is not connected!')
    } catch (error) {
        if (retries > 0) {
            await new Promise((resolve) => setTimeout(resolve, delay));
            return checkHealth(retries - 1, delay * 2);
        } else {
            throw error;
        }
    }
};

const makeRequest = async (method, route, formData) => {
    checkHealth();
    const optionalHeader = { headers: { 'Content-Type': 'multipart/form-data' } }
    let response = null;
    if (method === 'get') {
        response = await api.get(route);
    } else if (method === 'delete') {
        response = await api.delete(route);
    } else if (method === 'post') {
        response = await api.post(route, formData, optionalHeader);
        response = response.data;
    } else if (method === 'patch') {
        response = await api.patch(route, formData, optionalHeader);
        response = response.data;
    } else if (method === 'put') {
        response = await api.put(route, formData, optionalHeader);
        response = response.data;
    }
    return response;
}

export default makeRequest;
