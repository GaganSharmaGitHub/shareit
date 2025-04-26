import axios from 'axios';
import { toast } from 'svelte-toast';

// Set up Axios to include Authorization header from localStorage
axios.interceptors.request.use((config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

// Handle authentication errors globally
axios.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            toast.error('Authentication failed. Please log in again.');
            localStorage.clear();
        }
        return Promise.reject(error);
    }
);

const apiUtils = {
    async get(url: string, params: object = {}) {
        try {
            const response = await axios.get(url, { params });
            return response.data;
        } catch (error) {
            console.error('GET request failed:', error);
            throw error;
        }
    },

    async post(url: string, data: object) {
        try {
            const response = await axios.post(url, data);
            return response.data;
        } catch (error) {
            console.error('POST request failed:', error);
            throw error;
        }
    },

    async put(url: string, data: object) {
        try {
            const response = await axios.put(url, data);
            return response.data;
        } catch (error) {
            console.error('PUT request failed:', error);
            throw error;
        }
    },

    async postWithFile(url: string, file: File, additionalData: object = {}) {
        try {
            const formData = new FormData();
            formData.append('file', file);
            for (const key in additionalData) {
                formData.append(key, additionalData[key]);
            }

            const response = await axios.post(url, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            return response.data;
        } catch (error) {
            console.error('POST with file request failed:', error);
            throw error;
        }
    },
};

export default apiUtils;