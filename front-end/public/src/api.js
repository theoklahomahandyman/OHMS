import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL
});

const checkHealth = async (retries = 5, delay = 1000) => {
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

const submit_contact_form = async (formData) => {
    try {
        await checkHealth();
        const response = await api.post('/order/public/', formData);
        return response;
    } catch (error) {
        console.error('Failed to submit contact form:', error);
        throw error;
    }
};

export default submit_contact_form;
