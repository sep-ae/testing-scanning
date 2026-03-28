import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user:  JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    async login(email, password) {
    const res = await api.post('/auth/login', { email, password })
    this.token = res.data.token        // ← harus ada field 'token'
    this.user  = res.data.user
    localStorage.setItem('token', this.token)   // ← ini yang dipakai interceptor
    localStorage.setItem('user', JSON.stringify(this.user))
    },
    async register(username, email, password) {
      await api.post('/auth/register', { username, email, password })
    },
    logout() {
      this.token = null
      this.user  = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
})