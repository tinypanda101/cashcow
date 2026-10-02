/**
 * Single Shared Axios instance that every component can use to talk to the FastAPI backend
 */


import axios from 'axios';



// Axios.create builds a reusable preconfigured client
const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
});




// Request interceptor runs on every outoing request and checks if a token is sitting in local storage.
apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default apiClient;