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
const checkHealth = async (retries = 5, delay = 1500) => {
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
    url: '/user/admin/',
    createAdmin: async (data) => {
        try {
            return await makeRequest('post', adminAPI.url, data);
        } catch (error) {
            console.error('Error with adminAPI.createAdmin():', error);
            throw error;
        }
    },
    getAdmins: async () => {
        try {
            return await makeRequest('get', adminAPI.url);
        } catch (error) {
            console.error('Error with adminAPI.getAdmins():', error);
            throw error;
        }
    },
    updateAdmin: async (data) => {
        try {
            return await makeRequest('patch', `${adminAPI.url}${data.id}/`, data);
        } catch (error) {
            console.error('Error with adminAPI.updateAdmin():', error);
            throw error;
        }
    },
    deleteAdmin: async (adminID) => {
        try {
            return await makeRequest('delete', `${adminAPI.url}${adminID}/`);
        } catch (error) {
            console.error('Error with adminAPI.deleteAdmin():', error);
            throw error;
        }
    }
};

// Customer Routes
export const customerAPI = {
    url: '/customer/',
    createCustomer: async (data) => {
        try {
            return await makeRequest('post', customerAPI.url, data);
        } catch (error) {
            console.error('Error with customerAPI.createCustomer():', error);
            throw error;
        }
    },
    getCustomers: async () => {
        try {
            return await makeRequest('get', customerAPI.url);
        } catch (error) {
            console.error('Error with customerAPI.getCustomers():', error);
            throw error;
        }
    },
    updateCustomer: async (data) => {
        try {
            return await makeRequest('patch', `${customerAPI.url}${data.id}/`, data);
        } catch (error) {
            console.error('Error with customerAPI.updateCustomer():', error);
            throw error;
        }
    },
    deleteCustomer: async (customerID) => {
        try {
            return await makeRequest('delete', `${customerAPI.url}${customerID}/`);
        } catch (error) {
            console.error('Error with customerAPI.deleteCustomer():', error);
            throw error;
        }
    }
};

// Profile Routes
export const profileAPI = {
    url: '/user/',
    login: async (data) => {
        try {
            return await makeRequest('post', `${profileAPI.url}login/`, data);
        } catch (error) {
            console.error('Error with profileAPI.login():', error);
            throw error;
        }
    },
    refreshToken: async (data) => {
        try {
            return await makeRequest('post', '/token/refresh/', data);
        } catch (error) {
            console.error('Error with profileAPI.refreshToken():', error);
            throw error;
        }
    },
    getProfile: async () => {
        try {
            return await makeRequest('get', profileAPI.url);
        } catch (error) {
            console.error('Error with profileAPI.getProfile():', error);
            throw error;
        }
    },
    updateProfile: async (data) => {
        try {
            return await makeRequest('patch', profileAPI.url, data);
        } catch (error) {
            console.error('Error with profileAPI.updateProfile():', error);
            throw error;
        }
    },
    changePassword: async (data) => {
        try {
            return await makeRequest('patch', profileAPI.url, data);
        } catch (error) {
            console.error('Error with profileAPI.changePassword():', error);
            throw error;
        }
    }
};

// Service Routes
export const serviceAPI = {
    url: '/service/',
    createService: async (data) => {
        try {
            return await makeRequest('post', serviceAPI.url, data);
        } catch (error) {
            console.error('Error with serviceAPI.createService():', error);
            throw error;
        }
    },
    getServices: async () => {
        try {
            return await makeRequest('get', serviceAPI.url);
        } catch (error) {
            console.error('Error with serviceAPI.getServices():', error);
            throw error;
        }
    },
    updateService: async (data) => {
        try {
            return await makeRequest('patch', `${serviceAPI.url}${data.id}/`, data);
        } catch (error) {
            console.error('Error with serviceAPI.updateService():', error);
            throw error;
        }
    },
    deleteService: async (serviceID) => {
        try {
            return await makeRequest('delete', `${serviceAPI.url}${serviceID}/`);
        } catch (error) {
            console.error('Error with serviceAPI.deleteService():', error);
            throw error;
        }
    }
};

// Supplier Routes
export const supplierAPI = {
    url: '/supplier/',
    addressURL: '/addresses/',
    createSupplier: async (data) => {
        try {
            return await makeRequest('post', supplierAPI.url, data);
        } catch (error) {
            console.error('Error with supplierAPI.createSupplier():', error);
            throw error;
        }
    },
    getSuppliers: async () => {
        try {
            return await makeRequest('get', supplierAPI.url);
        } catch (error) {
            console.error('Error with supplierAPI.getSuppliers():', error);
            throw error;
        }
    },
    updateSupplier: async (data) => {
        try {
            return await makeRequest('patch', `${supplierAPI.url}${data.id}/`, data);
        } catch (error) {
            console.error('Error with supplierAPI.updateSupplier():', error);
            throw error;
        }
    },
    deleteSupplier: async (supplierID) => {
        try {
            return await makeRequest('delete', `${supplierAPI.url}${supplierID}/`);
        } catch (error) {
            console.error('Error with supplierAPI.deleteSupplier():', error);
            throw error;
        }
    },
    createAddress: async (supplierID, data) => {
        try {
            return await makeRequest('post', `${supplierAPI.url}${supplierID}/${supplierAPI.addressURL}`, data);
        } catch (error) {
            console.error('Error with supplierAPI.createAddress():', error);
            throw error;
        }
    },
    getAddresses: async (supplierID) => {
        try {
            return await makeRequest('post', `${supplierAPI.url}${supplierID}/${supplierAPI.addressURL}`);
        } catch (error) {
            console.error('Error with supplierAPI.getAddresses():', error);
            throw error;
        }
    },
    updateAddress: async (supplierID, addressID, data) => {
        try {
            return await makeRequest('patcj', `${supplierAPI.url}${supplierID}/${supplierAPI.addressURL}${addressID}/`, data);
        } catch (error) {
            console.error('Error with supplierAPI.updateAddress():', error);
            throw error;
        }
    },
    deleteAddress: async (supplierID, addressID) => {
        try {
            return await makeRequest('patcj', `${supplierAPI.url}${supplierID}/${supplierAPI.addressURL}${addressID}/`);
        } catch (error) {
            console.error('Error with supplierAPI.deleteAddress():', error);
            throw error;
        }
    },
};

// Material Routes
export const materialAPI = {
    url: '/inventory/material/',
    getMaterials: async () => {
        try {
            return await makeRequest('get', materialAPI.url);
        } catch (error) {
            console.error('Error with materialAPI.getMaterials():', error);
            throw error;
        }
    }
};

// Tool Routes
export const toolAPI = {
    url: '/inventory/tool/',
    getTools: async () => {
        try {
            return await makeRequest('get', toolAPI.url);
        } catch (error) {
            console.error('Error with toolAPI.getTools():', error);
            throw error;
        }
    }
};

// Order Routes
export const orderAPI = {

};

// Purchase Routes
export const purchaseAPI = {
    url: '/purchase/',
    materialURL: 'material/',
    toolURL: 'tool/',
    imageURL: 'image/',
    createPurchase: async (data) => {
        try {
            return await makeRequest('post', purchaseAPI.url, data);
        } catch (error) {
            console.error('Error with purchaseAPI.createPurchase():', error);
            throw error;
        }
    },
    getPurchases: async () => {
        try {
            return await makeRequest('get', purchaseAPI.url);
        } catch (error) {
            console.error('Error with purchaseAPI.getPurchases():', error);
            throw error;
        }
    },
    updatePurchase: async (purchaseID, data) => {
        try {
            return await makeRequest('patch', `${purchaseAPI.url}${purchaseID}/`, data);
        } catch (error) {
            console.error('Error with purchaseAPI.updatePurchase():', error);
            throw error;
        }
    },
    deletePurchase: async (purchaseID) => {
        try {
            return await makeRequest('delete', `${purchaseAPI.url}${purchaseID}/`);
        } catch (error) {
            console.error('Error with purchaseAPI.deletePurchase():', error);
            throw error;
        }
    },
    addMaterial: async (purchaseID, data) => {
        try {
            return await makeRequest('post', `${purchaseAPI.url}${purchaseAPI.materialURL}${purchaseID}/`, data);
        } catch (error) {
            console.error('Error with purchaseAPI.addMaterial():', error);
            throw error;
        }
    },
    addNewMaterial: async (purchaseID, data) => {
        try {
            return await makeRequest('post', `${purchaseAPI}new/${purchaseAPI.materialURL}${purchaseID}/`, data);
        } catch (error) {
            console.error('Error with purchaseAPI.addNewMaterial():', error);
            throw error;
        }
    },
    getMaterials: async (purchaseID) => {
        try {
            return await makeRequest('get', `${purchaseAPI.url}${purchaseAPI.materialURL}${purchaseID}/`);
        } catch (error) {
            console.error('Error with purchaseAPI.getMaterials():', error);
            throw error;
        }
    },
    updateMaterial: async (purchaseID, materialID, data) => {
        try {
            return await makeRequest('patch', `${purchaseAPI.url}${purchaseAPI.materialURL}${purchaseID}/${materialID}/`, data);
        } catch (error) {
            console.error('Error with purchaseAPI.updateMaterial():', error);
            throw error;
        }
    },
    deleteMaterial: async (purchaseID, materialID) => {
        try {
            return await makeRequest('delete', `${purchaseAPI.url}${purchaseAPI.materialURL}${purchaseID}/${materialID}/`);
        } catch (error) {
            console.error('Error with purchaseAPI.deleteMaterial():', error);
            throw error;
        }
    },
    addTool: async (purchaseID, data) => {
        try {
            return await makeRequest('post', `${purchaseAPI.url}${purchaseAPI.toolURL}${purchaseID}/`, data);
        } catch (error) {
            console.error('Error with purchaseAPI.addTool():', error);
            throw error;
        }
    },
    addNewTool: async (purchaseID, data) => {
        try {
            return await makeRequest('post', `${purchaseAPI}new/${purchaseAPI.toolURL}${purchaseID}/`, data);
        } catch (error) {
            console.error('Error with purchaseAPI.addNewMaterial():', error);
            throw error;
        }
    },
    getTools: async (purchaseID) => {
        try {
            return await makeRequest('get', `${purchaseAPI.url}${purchaseAPI.toolURL}${purchaseID}/`);
        } catch (error) {
            console.error('Error with purchaseAPI.getTools():', error);
            throw error;
        }
    },
    updateTool: async (purchaseID, toolID, data) => {
        try {
            return await makeRequest('patch', `${purchaseAPI.url}${purchaseAPI.toolURL}${purchaseID}/${toolID}/`, data);
        } catch (error) {
            console.error('Error with purchaseAPI.updateTool():', error);
            throw error;
        }
    },
    deleteTool: async (purchaseID, toolID) => {
        try {
            return await makeRequest('delete', `${purchaseAPI.url}${purchaseAPI.toolURL}${purchaseID}/${toolID}/`);
        } catch (error) {
            console.error('Error with purchaseAPI.deleteTool():', error);
            throw error;
        }
    },
    addReceipt: async (purchaseID, data) => {
        try {
            return await makeRequest('post', `${purchaseAPI.url}${purchaseAPI.imageURL}${purchaseID}/`, data, {
                headers: { 'Content-Type': 'multipart/form/data'}
            });
        } catch (error) {
            console.error('Error with purchaseAPI.addReceipt():', error);
            throw error;
        }
    },
    getReceipts: async (purchaseID) => {
        try {
            return await makeRequest('get', `${purchaseAPI.url}${purchaseAPI.imageURL}${purchaseID}/`);
        } catch (error) {
            console.error('Error with purchaseAPI.getReceipts():', error);
            throw error;
        }
    },
    deleteReceipt: async (purchaseID, receiptID) => {
        try {
            return await makeRequest('delete', `${purchaseAPI.url}${purchaseAPI.imageURL}${purchaseID}/${receiptID}/`);
        } catch (error) {
            console.error('Error with purchaseAPI.deleteReceipt():', error);
            throw error;
        }
    },
};
