/*
    Global Auth state using React's context API
*/
import {createContext, useContext, useMemo, useState} from 'react';
import apiClient from "../api/client";
 
// Create a global react context that acts as a central store for auth state without manual prop pass
const AuthContext = createContext(null);
 
//Extract and decode the user payload from JWT so that React can read it
//JWTs use base64url ('-' and '_'), which atob() can't read, so swap them first
function decodeToken(token) {
    const payloadSegment = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
    return JSON.parse(atob(payloadSegment));
}
 
//AuthProvider is a component that wraps the app and manages auth state
export function AuthProvider({ children }) {
    // Initalizing our token state from local storage to ensure a user stays logged in
    const [token, setToken] = useState(() => localStorage.getItem('access_token'));
 
    // Decode JWT into user object and cache the results
    const user = useMemo(() => (token ? decodeToken(token): null), [token]);
 
    //Sends credentials to the backend and saves BOTH tokens it returns
    const login = async (username, password) => {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
 
        const response = await apiClient.post('/auth/token', formData, {
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        });
 
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
        setToken(response.data.access_token);
    };
 
    //Tells the backend to invalidate the refresh token, then clears everything locally
    const logout = async () => {
        const refreshToken = localStorage.getItem('refresh_token');
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setToken(null);
        if (refreshToken) {
            await apiClient.post('/auth/logout', { refresh_token: refreshToken }).catch(() => {});
        }
    };
 
    //Bundles auth state variables and action functions into a single object
    const value = {
        token,
        user,
        isAuthenticated: Boolean(token),
        login,
        logout,
    };
 
    //Renders the context provider and passes down the value object to make the auth state and functions accessible throughout the app
    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}
 
//Custom React hook that exposes the AuthContext to any component
export function useAuth() {
    const context = useContext(AuthContext);
    if (context == null) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
}
