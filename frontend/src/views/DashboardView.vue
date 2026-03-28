<template>
  <div>

    <!-- Welcome Banner -->
    <div class="rounded-2xl p-6 mb-6 border relative overflow-hidden"
         style="background: linear-gradient(135deg, rgba(59,130,246,0.12), rgba(139,92,246,0.1)); border-color: rgba(59,130,246,0.15);">
      <div class="absolute right-6 top-4 text-5xl opacity-20">✍️</div>
      <p class="text-xs text-blue-500 font-medium mb-1">Dashboard</p>
      <h1 class="text-2xl font-bold text-gray-800">Halo, {{ auth.user?.username }}! 👋</h1>
      <p class="text-sm text-gray-400 mt-1">Kelola semua tulisan kamu di sini.</p>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-3 gap-4 mb-6">
      <div class="rounded-2xl p-5 text-center border"
           style="background: rgba(255,255,255,0.7); border-color: rgba(255,255,255,0.9); backdrop-filter: blur(10px);">
        <p class="text-3xl font-bold" style="background: linear-gradient(135deg, #3b82f6, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
          {{ myPosts.length }}
        </p>
        <p class="text-xs text-gray-400 mt-1">Total Post</p>
      </div>
      <div class="rounded-2xl p-5 text-center border"
           style="background: rgba(255,255,255,0.7); border-color: rgba(255,255,255,0.9); backdrop-filter: blur(10px);">
        <p class="text-3xl font-bold" style="background: linear-gradient(135deg, #10b981, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
          {{ thisMonth }}
        </p>
        <p class="text-xs text-gray-400 mt-1">Bulan Ini</p>
      </div>
      <div class="rounded-2xl p-5 text-center border"
           style="background: rgba(255,255,255,0.7); border-color: rgba(255,255,255,0.9); backdrop-filter: blur(10px);">
        <div class="w-7 h-7 rounded-full flex items-center justify-center text-sm text-white font-bold mx-auto mb-1"
             style="background: linear-gradient(135deg, #3b82f6, #8b5cf6);">
          {{ auth.user?.username?.charAt(0).toUpperCase() }}
        </div>
        <p class="text-xs text-gray-400">{{ auth.user?.username }}</p>
      </div>
    </div>

    <!-- My Posts -->
    <div class="rounded-2xl border overflow-hidden"
         style="background: rgba(255,255,255,0.75); border-color: rgba(255,255,255,0.9); backdrop-filter: blur(20px);">

      <!-- Header -->
      <div class="flex justify-between items-center px-6 py-4 border-b"
           style="border-color: rgba(0,0,0,0.05);">
        <h2 class="font-semibold text-gray-700 text-sm">Post Saya</h2>
        <RouterLink to="/create"
          class="px-3.5 py-1.5 rounded-xl text-xs font-semibold text-white"
          style="background: linear-gradient(135deg, #3b82f6, #8b5cf6);">
          + Buat Post
        </RouterLink>
      </div>

      <!-- Empty -->
      <div v-if="myPosts.length === 0" class="text-center py-12 text-gray-400">
        <div class="text-4xl mb-2">📭</div>
        <p class="text-sm">Belum ada post.</p>
        <RouterLink to="/create" class="text-xs text-blue-500 mt-1 inline-block">
          Tulis sekarang →
        </RouterLink>
      </div>

      <!-- List -->
      <div v-for="(post, i) in myPosts" :key="post.id"
        class="flex items-center justify-between px-6 py-4 transition-all"
        :style="i < myPosts.length - 1 ? 'border-bottom: 1px solid rgba(0,0,0,0.04)' : ''"
        onmouseover="this.style.background='rgba(59,130,246,0.03)'"
        onmouseout="this.style.background='transparent'">

        <div class="flex items-center gap-3 flex-1 min-w-0">
          <div class="w-8 h-8 rounded-lg flex items-center justify-center text-sm shrink-0"
               style="background: linear-gradient(135deg, rgba(59,130,246,0.12), rgba(139,92,246,0.12));">
            📝
          </div>
          <div class="min-w-0">
            <p class="text-sm font-medium text-gray-800 truncate cursor-pointer hover:text-blue-600 transition-colors"
               @click="$router.push(`/post/${post.id}`)">
              {{ post.title }}
            </p>
            <p class="text-xs text-gray-400 mt-0.5">{{ formatDate(post.created_at) }}</p>
          </div>
        </div>

        <div class="flex items-center gap-2 ml-4 shrink-0">
          <button @click="$router.push(`/post/${post.id}`)"
            class="px-3 py-1.5 rounded-lg text-xs border transition-all"
            style="color: #6b7280; border-color: rgba(0,0,0,0.08);"
            onmouseover="this.style.borderColor='rgba(59,130,246,0.3)'; this.style.color='#3b82f6'"
            onmouseout="this.style.borderColor='rgba(0,0,0,0.08)'; this.style.color='#6b7280'">
            Lihat
          </button>
          <button @click="confirmDelete(post.id)"
            class="px-3 py-1.5 rounded-lg text-xs border transition-all"
            style="color: #ef4444; border-color: rgba(239,68,68,0.15); background: rgba(239,68,68,0.04);"
            onmouseover="this.style.background='rgba(239,68,68,0.1)'"
            onmouseout="this.style.background='rgba(239,68,68,0.04)'">
            Hapus
          </button>
        </div>
      </div>
    </div>

    <!-- Confirm Delete Modal -->
    <div v-if="deleteId"
         class="fixed inset-0 z-50 flex items-center justify-center"
         style="background: rgba(0,0,0,0.3); backdrop-filter: blur(4px);">
      <div class="rounded-2xl p-6 w-80 border"
           style="background: rgba(255,255,255,0.97); box-shadow: 0 20px 60px rgba(0,0,0,0.15);">
        <div class="text-3xl text-center mb-3">⚠️</div>
        <h3 class="font-semibold text-gray-800 text-center mb-1">Hapus Post?</h3>
        <p class="text-xs text-gray-400 text-center mb-5">Tindakan ini tidak bisa dibatalkan.</p>
        <div class="flex gap-2">
          <button @click="deleteId = null"
            class="flex-1 py-2 rounded-xl text-sm border text-gray-500"
            style="border-color: rgba(0,0,0,0.1);">
            Batal
          </button>
          <button @click="doDelete"
            class="flex-1 py-2 rounded-xl text-sm font-medium text-white"
            style="background: linear-gradient(135deg, #ef4444, #dc2626);">
            Hapus
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api'

const auth     = useAuthStore()
const myPosts  = ref([])
const deleteId = ref(null)

const thisMonth = computed(() => {
  const now = new Date()
  return myPosts.value.filter(p => {
    if (!p.created_at) return false
    const d = new Date(p.created_at)
    return d.getMonth() === now.getMonth() && d.getFullYear() === now.getFullYear()
  }).length
})

onMounted(async () => {
  const res = await api.get('/posts/')
  myPosts.value = res.data.filter(p => p.author === auth.user?.username)
})

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' }) : '-'
}

function confirmDelete(id) { deleteId.value = id }

async function doDelete() {
  await api.delete(`/posts/${deleteId.value}`)
  myPosts.value = myPosts.value.filter(p => p.id !== deleteId.value)
  deleteId.value = null
}
</script>