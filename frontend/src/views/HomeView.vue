<template>
  <div class="max-w-3xl mx-auto p-4">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">VulnBlog</h1>
      <div v-if="auth.isLoggedIn" class="flex gap-2">
        <RouterLink to="/create" class="bg-blue-500 text-white px-3 py-1 rounded">+ Post</RouterLink>
        <button @click="auth.logout(); $router.push('/')" class="text-red-500">Logout</button>
      </div>
      <div v-else class="flex gap-2">
        <RouterLink to="/login" class="text-blue-500">Login</RouterLink>
        <RouterLink to="/register" class="text-blue-500">Register</RouterLink>
      </div>
    </div>

    <div v-for="post in posts" :key="post.id"
         class="border rounded p-4 mb-3 cursor-pointer hover:bg-gray-50"
         @click="$router.push(`/post/${post.id}`)">
      <h2 class="font-semibold text-lg">{{ post.title }}</h2>
      <p class="text-sm text-gray-500">by {{ post.author }} · {{ formatDate(post.created_at) }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api'

const posts = ref([])
const auth  = useAuthStore()

onMounted(async () => {
  const res = await api.get('/posts/')
  posts.value = res.data
})

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString('id-ID') : '-'
}
</script>