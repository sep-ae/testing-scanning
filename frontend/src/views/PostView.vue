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
        ← Back
      </button>

      <!-- Post Card -->
      <div class="rounded-2xl p-8 border"
           style="background: rgba(255,255,255,0.75); border-color: rgba(255,255,255,0.9); backdrop-filter: blur(20px); box-shadow: 0 8px 32px rgba(0,0,0,0.06);">

        <!-- Meta -->
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

        <!-- Owner Actions -->
        <div v-if="auth.user?.username === post.author"
             class="flex gap-2 mt-8 pt-6 border-t"
             style="border-color: rgba(0,0,0,0.06);">
          <button @click="confirmDelete"
            class="px-4 py-2 rounded-xl text-xs font-medium border transition-all"
            style="color: #ef4444; border-color: rgba(239,68,68,0.2); background: rgba(239,68,68,0.05);"
            onmouseover="this.style.background='rgba(239,68,68,0.1)'"
            onmouseout="this.style.background='rgba(239,68,68,0.05)'">
            🗑 Delete Post
          </button>
        </div>
      </div>

      <!-- Comments Section -->
      <div class="mt-8">
        <h2 class="text-lg font-semibold text-gray-800 mb-4">
          Comments <span class="text-sm font-normal text-gray-400">({{ comments.length }})</span>
        </h2>

        <!-- Comment Form -->
        <div v-if="auth.isLoggedIn"
             class="rounded-2xl p-5 border mb-6"
             style="background: rgba(255,255,255,0.75); border-color: rgba(255,255,255,0.9); backdrop-filter: blur(20px);">
          <div class="flex items-start gap-3">
            <div class="w-7 h-7 rounded-full flex items-center justify-center text-xs text-white font-semibold shrink-0 mt-0.5"
                 style="background: linear-gradient(135deg, #3b82f6, #8b5cf6);">
              {{ auth.user?.username?.charAt(0).toUpperCase() }}
            </div>
            <div class="flex-1">
              <textarea v-model="newComment"
                placeholder="Write a comment..."
                rows="3"
                class="w-full px-3 py-2 rounded-xl text-sm outline-none border transition-all resize-none"
                style="background: rgba(255,255,255,0.8); border-color: rgba(209,213,219,0.5);"
                @focus="$event.target.style.borderColor='rgba(59,130,246,0.4)'"
                @blur="$event.target.style.borderColor='rgba(209,213,219,0.5)'"></textarea>
              <div class="flex justify-end mt-2">
                <button @click="submitComment" :disabled="!newComment.trim() || submitting"
                  class="px-4 py-1.5 rounded-xl text-xs font-semibold text-white transition-all disabled:opacity-40"
                  style="background: linear-gradient(135deg, #3b82f6, #8b5cf6);">
                  {{ submitting ? 'Posting...' : 'Post Comment' }}
                </button>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="rounded-xl px-4 py-3 mb-6 text-sm text-gray-400 border"
             style="background: rgba(255,255,255,0.5); border-color: rgba(0,0,0,0.06);">
          <RouterLink to="/login" class="text-blue-500 hover:underline">Log in</RouterLink> to leave a comment.
        </div>

        <!-- Comment List -->
        <div v-if="comments.length === 0" class="text-center py-8 text-gray-400">
          <p class="text-sm">No comments yet. Be the first!</p>
        </div>

        <div v-for="comment in comments" :key="comment.id"
             class="rounded-2xl p-5 border mb-3 transition-all"
             style="background: rgba(255,255,255,0.7); border-color: rgba(255,255,255,0.9); backdrop-filter: blur(10px);">
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center gap-2">
              <div class="w-6 h-6 rounded-full flex items-center justify-center text-xs text-white font-semibold"
                   style="background: linear-gradient(135deg, #10b981, #3b82f6);">
                {{ comment.author?.charAt(0).toUpperCase() }}
              </div>
              <span class="text-sm font-medium text-gray-700">{{ comment.author }}</span>
              <span class="text-xs text-gray-300">{{ formatDate(comment.created_at) }}</span>
            </div>
            <button v-if="auth.user?.username === comment.author || auth.isAdmin"
              @click="deleteComment(comment.id)"
              class="text-xs text-gray-300 hover:text-red-500 transition-colors">
              ✕
            </button>
          </div>
          <!-- Comment content rendered as HTML to support rich text formatting -->
          <div class="text-sm text-gray-600 leading-relaxed" v-html="comment.content"></div>
        </div>
      </div>
    </div>

    <!-- Not found -->
    <div v-else class="text-center py-20 text-gray-400">
      <div class="text-5xl mb-3">🔍</div>
      <p class="font-medium">Post not found.</p>
      <button @click="$router.push('/posts')" class="text-sm text-blue-500 mt-2">← Back to Posts</button>
    </div>

    <!-- Confirm Delete Modal -->
    <div v-if="showConfirm"
         class="fixed inset-0 z-50 flex items-center justify-center"
         style="background: rgba(0,0,0,0.3); backdrop-filter: blur(4px);">
      <div class="rounded-2xl p-6 w-80 border"
           style="background: rgba(255,255,255,0.95); border-color: rgba(255,255,255,0.9); box-shadow: 0 20px 60px rgba(0,0,0,0.15);">
        <div class="text-3xl text-center mb-3">⚠️</div>
        <h3 class="font-semibold text-gray-800 text-center mb-1">Delete Post?</h3>
        <p class="text-xs text-gray-400 text-center mb-5">This action cannot be undone.</p>
        <div class="flex gap-2">
          <button @click="showConfirm = false"
            class="flex-1 py-2 rounded-xl text-sm border text-gray-500 transition-all"
            style="border-color: rgba(0,0,0,0.1);">
            Cancel
          </button>
          <button @click="deletePost"
            class="flex-1 py-2 rounded-xl text-sm font-medium text-white transition-all"
            style="background: linear-gradient(135deg, #ef4444, #dc2626);">
            Delete
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
import { toast } from 'vue-sonner'

const route       = useRoute()
const router      = useRouter()
const auth        = useAuthStore()
const post        = ref(null)
const loading     = ref(true)
const showConfirm = ref(false)
const comments    = ref([])
const newComment  = ref('')
const submitting  = ref(false)

onMounted(async () => {
  try {
    const res = await api.get(`/posts/${route.params.id}`)
    post.value = res.data
    await loadComments()
  } catch {
    post.value = null
  } finally {
    loading.value = false
  }
})

async function loadComments() {
  try {
    const res = await api.get(`/posts/${route.params.id}/comments`)
    comments.value = res.data
  } catch {
    comments.value = []
  }
}

async function submitComment() {
  if (!newComment.value.trim()) return
  submitting.value = true
  try {
    await api.post(`/posts/${route.params.id}/comments`, { content: newComment.value })
    newComment.value = ''
    await loadComments()
    toast.success('Komentar berhasil diposting!')
  } catch (e) {
    toast.error(e.response?.data?.message || 'Gagal memposting komentar')
  } finally {
    submitting.value = false
  }
}

async function deleteComment(commentId) {
  try {
    await api.delete(`/posts/comments/${commentId}`)
    comments.value = comments.value.filter(c => c.id !== commentId)
    toast.success('Komentar dihapus')
  } catch (e) {
    toast.error(e.response?.data?.message || 'Gagal menghapus komentar')
  }
}

function formatDate(d) {
  if (!d) return '-'
  return new Date(d).toLocaleDateString('en-US', { day: 'numeric', month: 'long', year: 'numeric' })
}

function confirmDelete() { showConfirm.value = true }

async function deletePost() {
  try {
    await api.delete(`/posts/${route.params.id}`)
    toast.success('Post dihapus')
    router.push('/posts')
  } catch (e) {
    toast.error('Gagal menghapus post')
  }
}
</script>