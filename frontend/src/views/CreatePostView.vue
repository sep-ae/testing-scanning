<template>
  <div class="max-w-2xl mx-auto">

    <!-- Header -->
    <div class="mb-6">
      <button @click="$router.back()"
        class="flex items-center gap-1.5 text-sm text-gray-400 mb-4 hover:text-blue-500 transition-colors">
        ← Kembali
      </button>
      <h1 class="text-2xl font-bold text-gray-800">Tulis Post Baru</h1>
      <p class="text-sm text-gray-400 mt-0.5">Bagikan ide dan cerita kamu</p>
    </div>

    <!-- Form Card -->
    <div class="rounded-2xl p-8 border"
         style="background: rgba(255,255,255,0.75); border-color: rgba(255,255,255,0.9); backdrop-filter: blur(20px); box-shadow: 0 8px 32px rgba(0,0,0,0.06);">

      <div class="space-y-4">
        <!-- Judul -->
        <div>
          <label class="text-xs font-medium text-gray-500 mb-1.5 block">Judul Post</label>
          <input v-model="title" placeholder="Tulis judul yang menarik..."
            class="w-full px-4 py-3 rounded-xl text-sm outline-none border transition-all font-medium"
            style="background: rgba(255,255,255,0.8); border-color: rgba(209,213,219,0.6);"
            @focus="$event.target.style.borderColor='rgba(59,130,246,0.5)'"
            @blur="$event.target.style.borderColor='rgba(209,213,219,0.6)'"/>
          <p class="text-xs text-gray-300 mt-1 text-right">{{ title.length }} karakter</p>
        </div>

        <!-- Konten -->
        <div>
          <label class="text-xs font-medium text-gray-500 mb-1.5 block">Konten</label>
          <textarea v-model="content" placeholder="Tulis konten post kamu di sini..."
            rows="10"
            class="w-full px-4 py-3 rounded-xl text-sm outline-none border transition-all resize-none leading-relaxed"
            style="background: rgba(255,255,255,0.8); border-color: rgba(209,213,219,0.6);"
            @focus="$event.target.style.borderColor='rgba(59,130,246,0.5)'"
            @blur="$event.target.style.borderColor='rgba(209,213,219,0.6)'"/>
          <p class="text-xs text-gray-300 mt-1 text-right">{{ content.length }} karakter</p>
        </div>
      </div>

      <!-- Error -->
      <div v-if="error"
           class="mt-4 px-3 py-2 rounded-lg text-xs text-red-600"
           style="background: rgba(239,68,68,0.08);">
        ⚠️ {{ error }}
      </div>

      <!-- Actions -->
      <div class="flex gap-3 mt-6">
        <button @click="$router.back()"
          class="px-5 py-2.5 rounded-xl text-sm border text-gray-500 transition-all"
          style="border-color: rgba(0,0,0,0.1);"
          onmouseover="this.style.background='rgba(0,0,0,0.03)'"
          onmouseout="this.style.background='transparent'">
          Batal
        </button>
        <button @click="submit" :disabled="loading"
          class="flex-1 py-2.5 rounded-xl text-sm font-semibold text-white transition-all duration-200"
          style="background: linear-gradient(135deg, #3b82f6, #8b5cf6); box-shadow: 0 4px 15px rgba(59,130,246,0.3);"
          onmouseover="this.style.transform='translateY(-1px)'"
          onmouseout="this.style.transform='translateY(0)'">
          {{ loading ? 'Mempublish...' : '🚀 Publish Post' }}
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const title   = ref('')
const content = ref('')
const error   = ref('')
const loading = ref(false)
const router  = useRouter()

async function submit() {
  if (!title.value.trim())   { error.value = 'Judul wajib diisi!'; return }
  if (!content.value.trim()) { error.value = 'Konten wajib diisi!'; return }

  loading.value = true
  error.value   = ''
  try {
    await api.post('/posts/', { title: title.value, content: content.value })
    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.message || 'Gagal mempublish post'
  } finally {
    loading.value = false
  }
}
</script>