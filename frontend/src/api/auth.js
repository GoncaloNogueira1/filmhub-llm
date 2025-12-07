import apiClient from './axios';
import useAuthStore from '../stores/authStore';
import useWatchlistStore from '../stores/watchlistStore';

const authAPI = {
  /**
   * Register new user
   * @param {Object} userData - {email, password, age?}
   * @returns {Promise}
   */
  register: async (userData) => {
    const response = await apiClient.post('/auth/register/', userData);
    return response.data;
  },

  /**
   * Login user
   * @param {Object} credentials - {email, password}
   * @returns {Promise}
   */
  login: async (credentials) => {
    const response = await apiClient.post('/auth/login/', credentials);
    const { user, tokens } = response.data;
    
    // Store in zustand
    useAuthStore.getState().login(user, tokens);
    
    return response.data;
  },

  /**
   * Logout user
   * @returns {Promise}
   */
  logout: async () => {
    const refreshToken = useAuthStore.getState().refreshToken;
    
    try {
      await apiClient.post('/auth/logout/', { refresh: refreshToken });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Always clear local state
      useAuthStore.getState().logout();
      useWatchlistStore.getState().clearWatchlist();
    }
  },

  /**
   * Get current user profile
   * @returns {Promise}
   */
  getProfile: async () => {
    const response = await apiClient.get('/auth/profile/');
    return response.data;
  },

  /**
   * Update user profile
   * @param {Object} profileData
   * @returns {Promise}
   */
  updateProfile: async (profileData) => {
    const response = await apiClient.patch('/auth/profile/', profileData);
    const updatedProfile = response.data.profile;
    
    // Update profile in store
    useAuthStore.getState().updateProfile(updatedProfile);
    
    // Update user in store with new name data
    const currentUser = useAuthStore.getState().user;
    if (currentUser) {
      const updatedUser = {
        ...currentUser,
        first_name: updatedProfile.first_name,
        last_name: updatedProfile.last_name,
        full_name: updatedProfile.full_name || currentUser.username
      };
      useAuthStore.getState().setUser(updatedUser);
    }
    
    return response.data;
  },
};

export default authAPI;
