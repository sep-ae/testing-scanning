<template>
  <div class="min-h-[80vh] flex items-center justify-center">
    <div class="w-full max-w-sm rounded-2xl p-8 border"
         style="background: rgba(255,255,255,0.75); border-color: rgba(255,255,255,0.9); backdrop-filter: blur(20px); box-shadow: 0 8px 32px rgba(0,0,0,0.06);">

      <!-- Icon -->
      <div class="w-12 h-12 rounded-2xl flex items-center justify-center text-xl mb-5 mx-auto"
           style="background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(59,130,246,0.15));">
        ✍️
      </div>

      <h2 class="text-xl font-bold text-gray-800 text-center mb-1">Buat Akun</h2>
      <p class="text-sm text-gray-400 text-center mb-6">Bergabung dan mulai menulis</p>

      <!-- Success -->
      <div v-if="success"
           class="mb-4 px-3 py-2.5 rounded-xl text-xs text-green-700 text-center"
           style="background: rgba(16,185,129,0.1);">
        ✅ Registrasi berhasil!
        <RouterLink to="/login" class="font-semibold underline ml-1">Login sekarang →</RouterLink>
      </div>

      <template v-if="!success">
        <!-- Form -->
        <div class="space-y-3">
          <div>
            <label class="text-xs font-medium text-gray-500 mb-1 block">Username</label>
            <input v-model="username" placeholder="username kamu"
              class="w-full px-4 py-2.5 rounded-xl text-sm outline-none transition-all border"
              style="background: rgba(255,255,255,0.8); border-color: rgba(209,213,219,0.6);"
              @focus="$event.target.style.borderColor='rgba(59,130,246,0.5)'"
              @blur="$event.target.style.borderColor='rgba(209,213,219,0.6)'"/>
          </div>
          <div>
            <label class="text-xs font-medium text-gray-500 mb-1 block">Email</label>
            <input v-model="email" type="email" placeholder="nama@email.com"
              class="w-full px-4 py-2.5 rounded-xl text-sm outline-none transition-all border"
              style="background: rgba(255,255,255,0.8); border-color: rgba(209,213,219,0.6);"
              @focus="$event.target.style.borderColor='rgba(59,130,246,0.5)'"
              @blur="$event.target.style.borderColor='rgba(209,213,219,0.6)'"/>
          </div>
          <div>
            <label class="text-xs font-medium text-gray-500 mb-1 block">Password</label>
            <input v-model="password" type="password" placeholder="••••••••"
              class="w-full px-4 py-2.5 rounded-xl text-sm outline-none transition-all border"
              style="background: rgba(255,255,255,0.8); border-color: rgba(209,213,219,0.6);"
              @focus="$event.target.style.borderColor='rgba(59,130,246,0.5)'"
              @blur="$event.target.style.borderColor='rgba(209,213,219,0.6)'"
              @keyup.enter="doRegister"/>
          </div>
        </div>

        <!-- Error -->
        <div v-if="error"
             class="mt-3 px-3 py-2 rounded-lg text-xs text-red-600"
             style="background: rgba(239,68,68,0.08);">
          ⚠️ {{ error }}
        </div>

        <!-- Button -->
        <button @click="doRegister" :disabled="loading"
          class="w-full mt-5 py-2.5 rounded-xl text-sm font-semibold text-white transition-all duration-200"
          style="background: linear-gradient(135deg, #10b981, #3b82f6); box-shadow: 0 4px 15px rgba(16,185,129,0.3);"
          onmouseover="this.style.transform='translateY(-1px)'"
          onmouseout="this.style.transform='translateY(0)'">
          {{ loading ? 'Mendaftar...' : 'Buat Akun' }}
        </button>

        <p class="text-xs text-center text-gray-400 mt-4">
          Sudah punya akun?
          <RouterLink to="/login" class="font-medium" style="color: #3b82f6;">Login</RouterLink>
        </p>
      </template>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'

const username = ref('')
const email    = ref('')
const password = ref('')
const error    = ref('')
const success  = ref(false)
const loading  = ref(false)
const auth     = useAuthStore()

async function doRegister() {
  if (!username.value || !email.value || !password.value) {
    error.value = 'Semua field wajib diisi'
    return
  }
  loading.value = true
  error.value   = ''
  try {
    await auth.register(username.value, email.value, password.value)
    success.value = true
  } catch (e) {
    error.value = e.response?.data?.message || 'Registrasi gagal'
  } finally {
    loading.value = false
  }
}
</script>