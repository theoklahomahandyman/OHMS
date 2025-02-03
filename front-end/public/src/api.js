import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL
});

const submit_contact_form = async (formData) => {
    const response = await api.post('/order/public/', formData);
    return response;
}

export default submit_contact_form;
