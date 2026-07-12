<template>
  <div>

    <!-- Header -->
    <div class="rounded-2xl p-6 mb-6 border relative overflow-hidden"
         style="background: linear-gradient(135deg, rgba(239,68,68,0.08), rgba(249,115,22,0.08)); border-color: rgba(239,68,68,0.12);">
      <div class="absolute right-6 top-4 text-5xl opacity-20">🛡️</div>
      <p class="text-xs text-red-500 font-medium mb-1">Admin Panel</p>
      <h1 class="text-2xl font-bold text-gray-800">Administration</h1>
      <p class="text-sm text-gray-400 mt-1">Manage users, posts, and comments.</p>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-3 gap-4 mb-6">
      <div class="rounded-2xl p-5 text-center border"
           style="background: rgba(255,255,255,0.7); border-color: rgba(255,255,255,0.9); backdrop-filter: blur(10px);">
        <p class="text-3xl font-bold" style="background: linear-gradient(135deg, #3b82f6, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
          {{ stats.total_users }}
        </p>
        <p class="text-xs text-gray-400 mt-1">Users</p>
      </div>
      <div class="rounded-2xl p-5 text-center border"
           style="background: rgba(255,255,255,0.7); border-color: rgba(255,255,255,0.9); backdrop-filter: blur(10px);">
        <p class="text-3xl font-bold" style="background: linear-gradient(135deg, #10b981, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
          {{ stats.total_posts }}
        </p>
        <p class="text-xs text-gray-400 mt-1">Posts</p>
      </div>
      <div class="rounded-2xl p-5 text-center border"
           style="background: rgba(255,255,255,0.7); border-color: rgba(255,255,255,0.9); backdrop-filter: blur(10px);">
        <p class="text-3xl font-bold" style="background: linear-gradient(135deg, #f59e0b, #ef4444); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
          {{ stats.total_comments }}
        </p>
        <p class="text-xs text-gray-400 mt-1">Comments</p>
      </div>
    </div>

    <!-- Tabs -->
    <div class="flex gap-1 mb-6 p-1 rounded-xl border"
         style="background: rgba(255,255,255,0.5); border-color: rgba(0,0,0,0.06);">
      <button v-for="tab in ['users', 'posts', 'comments']" :key="tab"
        @click="activeTab = tab"
        class="flex-1 py-2 rounded-lg text-sm font-medium transition-all"
        :style="activeTab === tab
          ? 'background: white; color: #1d4ed8; box-shadow: 0 2px 8px rgba(0,0,0,0.06);'
          : 'color: #9ca3af;'">
        {{ tab.charAt(0).toUpperCase() + tab.slice(1) }}
      </button>
    </div>

    <!-- Content Card -->
    <div class="rounded-2xl border overflow-hidden"
         style="background: rgba(255,255,255,0.75); border-color: rgba(255,255,255,0.9); backdrop-filter: blur(20px);">

      <!-- Users Tab -->
      <div v-if="activeTab === 'users'">
        <div class="px-6 py-4 border-b" style="border-color: rgba(0,0,0,0.05);">
          <h2 class="font-semibold text-gray-700 text-sm">All Users</h2>
        </div>
        <div v-if="users.length === 0" class="text-center py-12 text-gray-400 text-sm">No users found.</div>
        <div v-for="(user, i) in users" :key="user.id"
          class="flex items-center justify-between px-6 py-4 transition-all"
          :style="i < users.length - 1 ? 'border-bottom: 1px solid rgba(0,0,0,0.04)' : ''">
          <div class="flex items-center gap-3 flex-1 min-w-0">
            <div class="w-8 h-8 rounded-full flex items-center justify-center text-xs text-white font-semibold shrink-0"
                 :style="user.role === 'admin'
                   ? 'background: linear-gradient(135deg, #ef4444, #f59e0b);'
                   : 'background: linear-gradient(135deg, #3b82f6, #8b5cf6);'">
              {{ user.username?.charAt(0).toUpperCase() }}
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <p class="text-sm font-medium text-gray-800 truncate">{{ user.username }}</p>
                <span v-if="user.role === 'admin'"
                  class="px-1.5 py-0.5 rounded text-xs font-medium"
                  style="background: rgba(239,68,68,0.1); color: #ef4444;">admin</span>
              </div>
              <p class="text-xs text-gray-400 truncate">{{ user.email }} · {{ user.post_count }} posts · {{ user.comment_count }} comments</p>
            </div>
          </div>
          <div class="flex items-center gap-2 ml-4 shrink-0">
            <button @click="toggleRole(user)"
              class="px-3 py-1.5 rounded-lg text-xs border transition-all"
              :style="user.role === 'admin'
                ? 'color: #f59e0b; border-color: rgba(245,158,11,0.2); background: rgba(245,158,11,0.05);'
                : 'color: #3b82f6; border-color: rgba(59,130,246,0.2); background: rgba(59,130,246,0.05);'">
              {{ user.role === 'admin' ? 'Demote' : 'Promote' }}
            </button>
            <button @click="promptDeleteUser(user.id)"
              class="px-3 py-1.5 rounded-lg text-xs border transition-all"
              style="color: #ef4444; border-color: rgba(239,68,68,0.15); background: rgba(239,68,68,0.04);">
              Delete
            </button>
          </div>
        </div>
      </div>

      <!-- Posts Tab -->
      <div v-if="activeTab === 'posts'">
        <div class="px-6 py-4 border-b" style="border-color: rgba(0,0,0,0.05);">
          <h2 class="font-semibold text-gray-700 text-sm">All Posts</h2>
        </div>
        <div v-if="posts.length === 0" class="text-center py-12 text-gray-400 text-sm">No posts found.</div>
        <div v-for="(post, i) in posts" :key="post.id"
          class="flex items-center justify-between px-6 py-4 transition-all"
          :style="i < posts.length - 1 ? 'border-bottom: 1px solid rgba(0,0,0,0.04)' : ''">
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
              <p class="text-xs text-gray-400 mt-0.5">by {{ post.author }} · {{ post.comment_count }} comments · {{ formatDate(post.created_at) }}</p>
            </div>
          </div>
          <button @click="promptDeletePost(post.id)"
            class="px-3 py-1.5 rounded-lg text-xs border transition-all ml-4 shrink-0"
            style="color: #ef4444; border-color: rgba(239,68,68,0.15); background: rgba(239,68,68,0.04);">
            Delete
          </button>
        </div>
      </div>

      <!-- Comments Tab -->
      <div v-if="activeTab === 'comments'">
        <div class="px-6 py-4 border-b" style="border-color: rgba(0,0,0,0.05);">
          <h2 class="font-semibold text-gray-700 text-sm">All Comments</h2>
        </div>
        <div v-if="allComments.length === 0" class="text-center py-12 text-gray-400 text-sm">No comments found.</div>
        <div v-for="(comment, i) in allComments" :key="comment.id"
          class="flex items-center justify-between px-6 py-4 transition-all"
          :style="i < allComments.length - 1 ? 'border-bottom: 1px solid rgba(0,0,0,0.04)' : ''">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <span class="text-sm font-medium text-gray-700">{{ comment.author }}</span>
              <span class="text-xs text-gray-300">on</span>
              <span class="text-xs text-blue-500 cursor-pointer hover:underline truncate"
                    @click="$router.push(`/post/${comment.post_id}`)">
                {{ comment.post_title }}
              </span>
            </div>
            <p class="text-xs text-gray-500 truncate max-w-lg">{{ stripHtml(comment.content) }}</p>
            <p class="text-xs text-gray-300 mt-0.5">{{ formatDate(comment.created_at) }}</p>
          </div>
          <button @click="promptDeleteComment(comment.id)"
            class="px-3 py-1.5 rounded-lg text-xs border transition-all ml-4 shrink-0"
            style="color: #ef4444; border-color: rgba(239,68,68,0.15); background: rgba(239,68,68,0.04);">
            Delete
          </button>
        </div>
      </div>

    </div>

    <!-- Confirm Action Modal -->
    <div v-if="confirmModal.show"
         class="fixed inset-0 z-50 flex items-center justify-center"
         style="background: rgba(0,0,0,0.3); backdrop-filter: blur(4px);">
      <div class="rounded-2xl p-6 w-80 border"
           style="background: rgba(255,255,255,0.95); border-color: rgba(255,255,255,0.9); box-shadow: 0 20px 60px rgba(0,0,0,0.15);">
        <div class="text-3xl text-center mb-3">⚠️</div>
        <h3 class="font-semibold text-gray-800 text-center mb-1">{{ confirmModal.title }}</h3>
        <p class="text-xs text-gray-400 text-center mb-5">{{ confirmModal.message }}</p>
        <div class="flex gap-2">
          <button @click="confirmModal.show = false"
            class="flex-1 py-2 rounded-xl text-sm border text-gray-500 transition-all"
            style="border-color: rgba(0,0,0,0.1);">
            Batal
          </button>
          <button @click="executeConfirmAction"
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
import api from '../api'
import { toast } from 'vue-sonner'

const activeTab   = ref('users')
const stats       = ref({ total_users: 0, total_posts: 0, total_comments: 0 })
const users       = ref([])
const posts       = ref([])
const allComments = ref([])

const confirmModal = ref({
  show: false,
  title: '',
  message: '',
  action: null
})

onMounted(() => {
  loadAll()
})

async function loadAll() {
  try {
    const [s, u, p, c] = await Promise.all([
      api.get('/admin/stats'),
      api.get('/admin/users'),
      api.get('/admin/posts'),
      api.get('/admin/comments')
    ])
    stats.value       = s.data
    users.value       = u.data
    posts.value       = p.data
    allComments.value = c.data
  } catch (e) {
    toast.error(e.response?.data?.message || 'Gagal memuat data admin')
  }
}

async function toggleRole(user) {
  const newRole = user.role === 'admin' ? 'user' : 'admin'
  try {
    await api.patch(`/admin/users/${user.id}`, { role: newRole })
    user.role = newRole
    const s = await api.get('/admin/stats')
    stats.value = s.data
    toast.success(`Berhasil mengubah role ${user.username} menjadi ${newRole}`)
  } catch (e) {
    toast.error(e.response?.data?.message || 'Gagal mengubah role')
  }
}

function promptDeleteUser(id) {
  confirmModal.value = {
    show: true,
    title: 'Hapus User?',
    message: 'User dan semua kontennya (post & komentar) akan terhapus permanen.',
    action: () => deleteUser(id)
  }
}

async function deleteUser(id) {
  try {
    await api.delete(`/admin/users/${id}`)
    await loadAll()
    toast.success('User berhasil dihapus')
  } catch (e) {
    toast.error(e.response?.data?.message || 'Gagal menghapus user')
  } finally {
    confirmModal.value.show = false
  }
}

function promptDeletePost(id) {
  confirmModal.value = {
    show: true,
    title: 'Hapus Post?',
    message: 'Post ini akan terhapus secara permanen.',
    action: () => deletePost(id)
  }
}

async function deletePost(id) {
  try {
    await api.delete(`/admin/posts/${id}`)
    await loadAll()
    toast.success('Post berhasil dihapus')
  } catch (e) {
    toast.error(e.response?.data?.message || 'Gagal menghapus post')
  } finally {
    confirmModal.value.show = false
  }
}

function promptDeleteComment(id) {
  confirmModal.value = {
    show: true,
    title: 'Hapus Komentar?',
    message: 'Komentar ini akan terhapus secara permanen.',
    action: () => deleteComment(id)
  }
}

async function deleteComment(id) {
  try {
    await api.delete(`/admin/comments/${id}`)
    await loadAll()
    toast.success('Komentar berhasil dihapus')
  } catch (e) {
    toast.error(e.response?.data?.message || 'Gagal menghapus komentar')
  } finally {
    confirmModal.value.show = false
  }
}

function executeConfirmAction() {
  if (confirmModal.value.action) {
    confirmModal.value.action()
  }
}

function stripHtml(html) {
  const tmp = document.createElement('div')
  tmp.innerHTML = html
  return tmp.textContent || tmp.innerText || ''
}

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' }) : '-'
}
</script>
