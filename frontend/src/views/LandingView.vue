<template>
  <div class="min-h-screen" style="background: linear-gradient(135deg, #f0f4ff 0%, #faf5ff 50%, #f0fdf4 100%);">
    <Navbar />

    <!-- Hero -->
    <section class="max-w-5xl mx-auto px-6 pt-24 pb-20 text-center">

      <!-- Badge -->
      <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-medium mb-6 border"
           style="background: rgba(59,130,246,0.08); color: #2563eb; border-color: rgba(59,130,246,0.2);">
        ✨ Platform Blog Open Source
      </div>

      <h1 class="text-5xl font-bold mb-5 leading-tight"
          style="background: linear-gradient(135deg, #1e40af, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        Tulis. Bagikan.<br/>Inspirasi.
      </h1>

      <p class="text-gray-400 text-lg mb-10 max-w-md mx-auto leading-relaxed">
        Platform blog minimalis untuk berbagi tulisan, ide, dan cerita kamu.
      </p>

      <div class="flex justify-center gap-3">
        <RouterLink to="/posts"
          class="px-6 py-2.5 rounded-xl text-sm font-semibold text-white transition-all duration-200 shadow-md"
          style="background: linear-gradient(135deg, #3b82f6, #8b5cf6); box-shadow: 0 4px 15px rgba(59,130,246,0.3);"
          onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 6px 20px rgba(59,130,246,0.4)'"
          onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(59,130,246,0.3)'">
          Baca Post
        </RouterLink>
        <RouterLink to="/register"
          class="px-6 py-2.5 rounded-xl text-sm font-semibold border transition-all duration-200"
          style="background: rgba(255,255,255,0.7); color: #3b82f6; border-color: rgba(59,130,246,0.25); backdrop-filter: blur(10px);"
          onmouseover="this.style.background='rgba(255,255,255,0.9)'"
          onmouseout="this.style.background='rgba(255,255,255,0.7)'">
          Mulai Nulis →
        </RouterLink>
      </div>

      <!-- Stats -->
      <div class="flex justify-center gap-8 mt-14">
        <div v-for="stat in stats" :key="stat.label" class="text-center">
          <p class="text-2xl font-bold" style="color: #1e40af;">{{ stat.value }}</p>
          <p class="text-xs text-gray-400 mt-0.5">{{ stat.label }}</p>
        </div>
      </div>
    </section>

    <!-- Latest Posts -->
    <section class="max-w-5xl mx-auto px-6 pb-20">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-lg font-semibold text-gray-700">Post Terbaru</h2>
        <RouterLink to="/posts" class="text-sm font-medium" style="color: #3b82f6;">
          Lihat semua →
        </RouterLink>
      </div>

      <div class="grid md:grid-cols-3 gap-4">
        <div v-for="post in latestPosts" :key="post.id"
          class="rounded-2xl p-5 cursor-pointer transition-all duration-200 border"
          style="background: rgba(255,255,255,0.7); border-color: rgba(255,255,255,0.9); backdrop-filter: blur(10px);"
          onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.08)'"
          onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'"
          @click="$router.push(`/post/${post.id}`)">

          <!-- Icon placeholder -->
          <div class="w-8 h-8 rounded-lg flex items-center justify-center text-sm mb-3"
               style="background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(139,92,246,0.15));">
            📝
          </div>

          <h3 class="font-semibold text-gray-800 mb-1 text-sm leading-snug">{{ post.title }}</h3>
          <p class="text-xs text-gray-400">by {{ post.author }}</p>
        </div>

        <!-- Empty state -->
        <div v-if="latestPosts.length === 0"
          class="col-span-3 text-center py-12 text-gray-400 text-sm">
          Belum ada post. <RouterLink to="/register" class="text-blue-500">Jadilah yang pertama!</RouterLink>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="border-t text-center py-6 text-xs text-gray-400"
            style="border-color: rgba(0,0,0,0.06);">
      VulnBlog © 2026 · Dibuat untuk keperluan pengujian keamanan
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Navbar from '../components/Navbar.vue'
import api from '../api'

const latestPosts = ref([])
const stats = ref([
  { value: '0', label: 'Post' },
  { value: '∞', label: 'Ide' },
  { value: '100%', label: 'Open' },
])

onMounted(async () => {
  try {
    const res = await api.get('/posts/')
    latestPosts.value = res.data.slice(0, 3)
    stats.value[0].value = res.data.length + '+'
  } catch {}
})
</script>