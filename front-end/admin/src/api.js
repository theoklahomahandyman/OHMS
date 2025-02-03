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

const makeRequest = async (method, route, formData) => {
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
