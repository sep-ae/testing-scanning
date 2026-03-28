<template>
  <div class="min-h-[80vh] flex items-center justify-center">
    <div class="w-full max-w-sm rounded-2xl p-8 border"
         style="background: rgba(255,255,255,0.75); border-color: rgba(255,255,255,0.9); backdrop-filter: blur(20px); box-shadow: 0 8px 32px rgba(0,0,0,0.06);">

      <!-- Icon -->
      <div class="w-12 h-12 rounded-2xl flex items-center justify-center text-xl mb-5 mx-auto"
           style="background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(139,92,246,0.15));">
        🔐
      </div>

      <h2 class="text-xl font-bold text-gray-800 text-center mb-1">Selamat Datang</h2>
      <p class="text-sm text-gray-400 text-center mb-6">Login ke akun VulnBlog kamu</p>

      <!-- Form -->
      <div class="space-y-3">
        <div>
          <label class="text-xs font-medium text-gray-500 mb-1 block">Email</label>
          <input v-model="email" type="email" placeholder="nama@email.com"
            class="w-full px-4 py-2.5 rounded-xl text-sm outline-none transition-all border"
            style="background: rgba(255,255,255,0.8); border-color: rgba(209,213,219,0.6);"
            @focus="$event.target.style.borderColor='rgba(59,130,246,0.5)'"
            @blur="$event.target.style.borderColor='rgba(209,213,219,0.6)'"
            @keyup.enter="doLogin"/>
        </div>
        <div>
          <label class="text-xs font-medium text-gray-500 mb-1 block">Password</label>
          <input v-model="password" type="password" placeholder="••••••••"
            class="w-full px-4 py-2.5 rounded-xl text-sm outline-none transition-all border"
            style="background: rgba(255,255,255,0.8); border-color: rgba(209,213,219,0.6);"
            @focus="$event.target.style.borderColor='rgba(59,130,246,0.5)'"
            @blur="$event.target.style.borderColor='rgba(209,213,219,0.6)'"
            @keyup.enter="doLogin"/>
        </div>
      </div>

      <!-- Error -->
      <div v-if="error"
           class="mt-3 px-3 py-2 rounded-lg text-xs text-red-600"
           style="background: rgba(239,68,68,0.08);">
        ⚠️ {{ error }}
      </div>

      <!-- Button -->
      <button @click="doLogin" :disabled="loading"
        class="w-full mt-5 py-2.5 rounded-xl text-sm font-semibold text-white transition-all duration-200"
        style="background: linear-gradient(135deg, #3b82f6, #8b5cf6); box-shadow: 0 4px 15px rgba(59,130,246,0.3);"
        onmouseover="this.style.transform='translateY(-1px)'"
        onmouseout="this.style.transform='translateY(0)'">
        {{ loading ? 'Masuk...' : 'Login' }}
      </button>

      <p class="text-xs text-center text-gray-400 mt-4">
        Belum punya akun?
        <RouterLink to="/register" class="font-medium" style="color: #3b82f6;">Register</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const email    = ref('')
const password = ref('')
const error    = ref('')
const loading  = ref(false)
const router   = useRouter()
const route    = useRoute()
const auth     = useAuthStore()

async function doLogin() {
  if (!email.value || !password.value) {
    error.value = 'Email dan password wajib diisi'
    return
  }
  loading.value = true
  error.value   = ''
  try {
    await auth.login(email.value, password.value)
    const next = route.query.next || '/'
    router.push(next)
  } catch {
    error.value = 'Email atau password salah'
  } finally {
    loading.value = false
  }
}
</script>