/**
 * Single Shared Axios instance that every component can use to talk to the FastAPI backend
 */

import axios from 'axios';
 
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
 
// Axios.create builds a reusable preconfigured client
const apiClient = axios.create({ baseURL });
 
// A second client with NO interceptors, used only for /auth/refresh.
// If the refresh itself fails with 401, it won't try to refresh again (no infinite loop).
const refreshClient = axios.create({ baseURL });
 
 
// Request interceptor runs on every outgoing request and checks if a token is sitting in local storage.
apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});
 
 
// If several requests fail at the same time, they all wait on this one refresh
// instead of each starting their own.
let refreshPromise = null;
 
function refreshTokens() {
    if (!refreshPromise) {
        refreshPromise = refreshClient
            .post('/auth/refresh', { refresh_token: localStorage.getItem('refresh_token') })
            .then((response) => {
                localStorage.setItem('access_token', response.data.access_token);
                localStorage.setItem('refresh_token', response.data.refresh_token);
            })
            .catch((error) => {
                // Refresh failed: the session is over. Clear tokens and go to login.
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
                throw error;
            })
            .finally(() => {
                refreshPromise = null;
            });
    }
    return refreshPromise;
}
 
 
// Response interceptor: on a 401, refresh the tokens once and retry the request.
apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const request = error.config;
 
        // Don't refresh if:
        // - it's not a 401
        // - we already retried this request once
        // - it's the login request (a 401 there means a wrong password)
        if (error.response?.status !== 401 || request._retry || request.url === '/auth/token') {
            return Promise.reject(error);
        }
 
        request._retry = true;
        await refreshTokens();       // throws (and redirects) if the refresh fails
        return apiClient(request);   // retry with the new access token
    },
);
 
export default apiClient;
