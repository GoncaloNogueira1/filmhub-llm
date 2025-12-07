import { create } from 'zustand';

export const useAuthStore = create((set, get) => ({
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  accessToken: localStorage.getItem('accessToken') || null,
  refreshToken: localStorage.getItem('refreshToken') || null,
  profile: null,
  isAuthenticated: !!localStorage.getItem('accessToken'),

  login: (user, tokens) => {
    const { access, refresh } = tokens;
    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    localStorage.setItem('user', JSON.stringify(user));
    set({ 
      user, 
      accessToken: access, 
      refreshToken: refresh, 
      isAuthenticated: true 
    });
  },

  logout: () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    set({ 
      user: null, 
      accessToken: null, 
      refreshToken: null, 
      profile: null, 
      isAuthenticated: false 
    });
  },

  updateToken: (accessToken) => {
    localStorage.setItem('accessToken', accessToken);
    set({ accessToken });
  },

  updateProfile: (profile) => {
    set({ profile });
  },

  setUser: (user) => {
    localStorage.setItem('user', JSON.stringify(user));
    set({ user });
  },
}));

export default useAuthStore;