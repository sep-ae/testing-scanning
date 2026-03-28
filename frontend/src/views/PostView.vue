<template>
  <div class="max-w-2xl mx-auto">

    <!-- Loading -->
    <div v-if="loading" class="space-y-4 animate-pulse">
      <div class="h-6 rounded-xl w-3/4" style="background: rgba(0,0,0,0.08);"></div>
      <div class="h-4 rounded-lg w-1/3" style="background: rgba(0,0,0,0.05);"></div>
      <div class="h-40 rounded-2xl" style="background: rgba(0,0,0,0.05);"></div>
    </div>

    <!-- Content -->
    <div v-else-if="post">
      <!-- Back -->
      <button @click="$router.back()"
        class="flex items-center gap-1.5 text-sm text-gray-400 mb-6 hover:text-blue-500 transition-colors">
        ← Kembali
      </button>

      <!-- Card -->
      <div class="rounded-2xl p-8 border"
           style="background: rgba(255,255,255,0.75); border-color: rgba(255,255,255,0.9); backdrop-filter: blur(20px); box-shadow: 0 8px 32px rgba(0,0,0,0.06);">

        <!-- Meta atas -->
        <div class="flex items-center gap-2 mb-4">
          <div class="w-7 h-7 rounded-full flex items-center justify-center text-xs text-white font-semibold"
               style="background: linear-gradient(135deg, #3b82f6, #8b5cf6);">
            {{ post.author?.charAt(0).toUpperCase() }}
          </div>
          <span class="text-sm text-gray-500">{{ post.author }}</span>
          <span class="text-gray-200">·</span>
          <span class="text-xs text-gray-400">{{ formatDate(post.created_at) }}</span>
        </div>

        <!-- Title -->
        <h1 class="text-2xl font-bold text-gray-800 mb-6 leading-snug">
          {{ post.title }}
        </h1>

        <!-- Divider -->
        <div class="h-px mb-6" style="background: rgba(0,0,0,0.06);"></div>

        <!-- Content -->
        <div class="text-gray-600 text-sm leading-relaxed whitespace-pre-wrap">
          {{ post.content }}
        </div>

        <!-- Action (kalau pemilik) -->
        <div v-if="auth.user?.username === post.author"
             class="flex gap-2 mt-8 pt-6 border-t"
             style="border-color: rgba(0,0,0,0.06);">
          <button @click="confirmDelete"
            class="px-4 py-2 rounded-xl text-xs font-medium border transition-all"
            style="color: #ef4444; border-color: rgba(239,68,68,0.2); background: rgba(239,68,68,0.05);"
            onmouseover="this.style.background='rgba(239,68,68,0.1)'"
            onmouseout="this.style.background='rgba(239,68,68,0.05)'">
            🗑 Hapus Post
          </button>
        </div>
      </div>
    </div>

    <!-- Not found -->
    <div v-else class="text-center py-20 text-gray-400">
      <div class="text-5xl mb-3">🔍</div>
      <p class="font-medium">Post tidak ditemukan.</p>
      <button @click="$router.push('/posts')" class="text-sm text-blue-500 mt-2">← Kembali ke Posts</button>
    </div>

    <!-- Confirm Delete Modal -->
    <div v-if="showConfirm"
         class="fixed inset-0 z-50 flex items-center justify-center"
         style="background: rgba(0,0,0,0.3); backdrop-filter: blur(4px);">
      <div class="rounded-2xl p-6 w-80 border"
           style="background: rgba(255,255,255,0.95); border-color: rgba(255,255,255,0.9); box-shadow: 0 20px 60px rgba(0,0,0,0.15);">
        <div class="text-3xl text-center mb-3">⚠️</div>
        <h3 class="font-semibold text-gray-800 text-center mb-1">Hapus Post?</h3>
        <p class="text-xs text-gray-400 text-center mb-5">Tindakan ini tidak bisa dibatalkan.</p>
        <div class="flex gap-2">
          <button @click="showConfirm = false"
            class="flex-1 py-2 rounded-xl text-sm border text-gray-500 transition-all"
            style="border-color: rgba(0,0,0,0.1);">
            Batal
          </button>
          <button @click="deletePost"
            class="flex-1 py-2 rounded-xl text-sm font-medium text-white transition-all"
            style="background: linear-gradient(135deg, #ef4444, #dc2626);">
            Hapus
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api'

const route       = useRoute()
const router      = useRouter()
const auth        = useAuthStore()
const post        = ref(null)
const loading     = ref(true)
const showConfirm = ref(false)

onMounted(async () => {
  try {
    const res = await api.get(`/posts/${route.params.id}`)
    post.value = res.data
  } catch {
    post.value = null
  } finally {
    loading.value = false
  }
})

function formatDate(d) {
  if (!d) return '-'
  return new Date(d).toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' })
}

function confirmDelete() { showConfirm.value = true }

async function deletePost() {
  await api.delete(`/posts/${route.params.id}`)
  router.push('/posts')
}
</script>