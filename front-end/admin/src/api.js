import { ACCESS_TOKEN } from './constants';
import Cookies from 'js-cookie';
import axios from 'axios';

// Create API instance with base configuration
const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL
});

// Global request interceptor for auth headers
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
);

// Global response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            Cookies.remove(ACCESS_TOKEN);
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// Wake back-end and database
const checkHealth = async (retries = 5, delay = 1000) => {
    try {
        const response = await api.get('/health/check/');
        if (response.data.status === 'ready') return true;
        throw new Error('Back-End is not connected!')
    } catch (error) {
        if (retries <= 0) {
            console.error(error);
            throw new Error('Service unavailable');
        }
        await new Promise((resolve) => setTimeout(resolve, delay));
        return checkHealth(retries - 1, delay * 2);
    }
};

// Initialize app health check once
let isHealthy = false;
export const initializeAPI = async () => {
    if (!isHealthy) {
        isHealthy = await checkHealth();
    }
    return isHealthy;
};

// Unified request handler
export const makeRequest = async (method, url, data = null) => {
    if (!isHealthy) await initializeAPI();
    const config = {};
    if (data instanceof FormData) {
        config.headers = { 'Content-type': 'multipart/form-data' };
    }
    try {
        const response = await api({ method, url, data, ...config });
        return response.data;
    } catch (error) {
        console.error(`API Error [${method.toUpperCase()} ${url}]:`, error);
        if (!error.message) {
            error.message = 'Network error - please check your connection';
        }
        throw error;
    }
};

// Admin Routes
export const adminAPI = {
    createAdmin: async (data) => {
        try {
            const response = await makeRequest('post', '/user/admin', data);
            return response.data;
        } catch (error) {
            console.error('Error with adminAPI.createAdmin():', error);
            throw error;
        }
    },
    getAdmin: async (adminID) => {
        try {
            const response = await makeRequest('get', `/user/admin/${adminID}/`);
            return response.data;
        } catch (error) {
            console.error('Error with adminAPI.getAdmin():', error);
            throw error;
        }
    },
    getAdmins: async () => {
        try {
            const response = await makeRequest('get', '/user/admin');
            return response.data;
        } catch (error) {
            console.error('Error with adminAPI.getAdmins():', error);
            throw error;
        }
    },
    updateAdmin: async (data) => {
        try {
            const response = await makeRequest('patch', `/user/admin/${data.id}`, data);
            return response.data;
        } catch (error) {
            console.error('Error with adminAPI.updateAdmin():', error);
            throw error;
        }
    },
    deleteAdmin: async (adminID) => {
        try {
            const response = await makeRequest('delete', `/user/admin/${adminID}/`);
            return response.data;
        } catch (error) {
            console.error('Error with adminAPI.deleteAdmin():', error);
            throw error;
        }
    }
};

// Customer Routes
export const customerAPI = {

};

// Profile Routes
export const profileAPI = {

};

// Service Routes
export const serviceAPI = {

};

// Supplier Routes
export const supplierAPI = {

};

// Material Routes
export const materialAPI = {

};

// Tool Routes
export const toolAPI = {

};

// Order Routes
export const orderAPI = {

};

// Purchase Routes
export const purchaseAPI = {

};
