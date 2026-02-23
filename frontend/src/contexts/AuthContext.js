/**
 * Authentication Context
 * Manages login state, user data, and token management
 */

import React, { createContext, useState, useEffect, useCallback } from 'react';
import apiService from '../services/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check if user is already logged in
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('access_token');
      const storedUser = localStorage.getItem('user');

      if (token && storedUser) {
        try {
          const response = await apiService.getMe();
          if (response.data.success) {
            setUser(response.data.user);
            setProfile(response.data.profile);
            setIsAuthenticated(true);
          }
        } catch (err) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('user');
          setIsAuthenticated(false);
        }
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const signup = useCallback(async (email, password, name) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiService.signup({ email, password, name });
      if (response.data.success) {
        const token = response.data.access_token;
        const user = response.data.user;
        localStorage.setItem('access_token', token);
        localStorage.setItem('user', JSON.stringify(user));
        setUser(user);
        // Initialize empty profile
        setProfile({
          id: null,
          user_id: user.id,
          skills: {
            coding: 3,
            math: 3,
            creativity: 3,
            communication: 3,
            leadership: 3,
            domain_expertise: 2
          },
          preferred_domains: [],
          career_goal: null,
          teamwork_preference: true,
          project_experience: 2,
          work_environment: null,
          motivation: null,
          confidence: 2,
          completed: false
        });
        setIsAuthenticated(true);
        return { success: true, message: 'Signup successful' };
      }
      return { success: false, error: 'Signup failed' };
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Signup failed';
      setError(errorMsg);
      setIsAuthenticated(false);
      return { success: false, error: errorMsg };
    } finally {
      setIsLoading(false);
    }
  }, []);

  const login = useCallback(async (email, password) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiService.login(email, password);
      if (response.data.success) {
        const token = response.data.access_token;
        const user = response.data.user;
        localStorage.setItem('access_token', token);
        localStorage.setItem('user', JSON.stringify(user));
        setUser(user);
        setIsAuthenticated(true);
        
        // Load profile if available
        try {
          const profileResponse = await apiService.getProfile();
          if (profileResponse.data.success && profileResponse.data.profile) {
            setProfile(profileResponse.data.profile);
          }
        } catch (err) {
          console.warn('Could not load profile:', err);
        }
        
        return { success: true, message: 'Login successful' };
      }
      return { success: false, error: 'Login failed' };
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Login failed';
      setError(errorMsg);
      setIsAuthenticated(false);
      return { success: false, error: errorMsg };
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      await apiService.logout();
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      setUser(null);
      setProfile(null);
      setIsAuthenticated(false);
    }
  }, []);

  const updateProfile = useCallback(async (profileData) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiService.updateProfile(profileData);
      if (response.data.success) {
        setProfile(response.data.profile);
        return { success: true, profile: response.data.profile };
      }
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Profile update failed';
      setError(errorMsg);
      return { success: false, error: errorMsg };
    } finally {
      setIsLoading(false);
    }
  }, []);

  const value = {
    user,
    profile,
    isAuthenticated,
    isLoading,
    error,
    signup,
    login,
    logout,
    updateProfile,
    clearError: () => setError(null),
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = React.useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
