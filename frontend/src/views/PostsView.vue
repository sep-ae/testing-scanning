<template>
  <div>
    <!-- Header -->
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">Semua Post</h1>
        <p class="text-sm text-gray-400 mt-0.5">{{ filtered.length }} tulisan tersedia</p>
      </div>
      <RouterLink to="/create"
        class="px-4 py-2 rounded-xl text-sm font-semibold text-white"
        style="background: linear-gradient(135deg, #3b82f6, #8b5cf6); box-shadow: 0 4px 15px rgba(59,130,246,0.3);">
        + Tulis Post
      </RouterLink>
    </div>

    <!-- Search Bar -->
    <div class="relative mb-6">
      <span class="absolute left-4 top-1/2 -translate-y-1/2 text-sm">
        {{ loading ? '⏳' : '🔍' }}
      </span>
      <input v-model="query"
        placeholder="Cari post..."
        class="w-full pl-10 pr-4 py-2.5 rounded-xl text-sm outline-none border transition-all"
        style="background: rgba(255,255,255,0.75); border-color: rgba(209,213,219,0.5); backdrop-filter: blur(10px);"
        @focus="$event.target.style.borderColor='rgba(59,130,246,0.4)'"
        @blur="$event.target.style.borderColor='rgba(209,213,219,0.5)'"/>
      <button v-if="query" @click="clearSearch"
        class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 text-xs">
        ✕
      </button>
    </div>

    <!-- Search info -->
    <div v-if="query && !loading" class="mb-4 text-xs text-gray-400">
      {{ filtered.length }} hasil untuk "<span class="text-blue-500">{{ query }}</span>"
    </div>

    <!-- Empty State -->
    <div v-if="filtered.length === 0 && !loading" class="text-center py-20 text-gray-400">
      <div class="text-5xl mb-4">{{ query ? '🔍' : '📭' }}</div>
      <p class="font-medium">
        {{ query ? `Tidak ada hasil untuk "${query}"` : 'Belum ada post.' }}
      </p>
      <button v-if="query" @click="clearSearch"
        class="text-sm text-blue-500 mt-2 inline-block">
        Hapus pencarian
      </button>
      <RouterLink v-else to="/create" class="text-sm text-blue-500 mt-2 inline-block">
        Jadilah yang pertama nulis →
      </RouterLink>
    </div>

    <!-- Loading skeleton -->
    <div v-if="loading" class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="i in 3" :key="i"
        class="rounded-2xl p-5 border animate-pulse"
        style="background: rgba(255,255,255,0.7); border-color: rgba(255,255,255,0.9);">
        <div class="w-9 h-9 rounded-xl mb-4" style="background: rgba(0,0,0,0.07);"></div>
        <div class="h-4 rounded-lg mb-2 w-3/4" style="background: rgba(0,0,0,0.07);"></div>
        <div class="h-3 rounded-lg w-1/2" style="background: rgba(0,0,0,0.04);"></div>
      </div>
    </div>

    <!-- Grid -->
    <div v-if="!loading" class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="post in filtered" :key="post.id"
        class="rounded-2xl p-5 cursor-pointer transition-all duration-200 border"
        style="background: rgba(255,255,255,0.7); border-color: rgba(255,255,255,0.9); backdrop-filter: blur(10px);"
        onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.08)'"
        onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'"
        @click="$router.push(`/post/${post.id}`)">

        <div class="w-9 h-9 rounded-xl flex items-center justify-center text-base mb-4"
             style="background: linear-gradient(135deg, rgba(59,130,246,0.12), rgba(139,92,246,0.12));">
          📝
        </div>
        <h2 class="font-semibold text-gray-800 text-sm leading-snug mb-2 line-clamp-2">
          {{ post.title }}
        </h2>
        <div class="flex items-center justify-between mt-3 pt-3 border-t"
             style="border-color: rgba(0,0,0,0.06);">
          <div class="flex items-center gap-1.5">
            <div class="w-5 h-5 rounded-full flex items-center justify-center text-xs text-white font-semibold"
                 style="background: linear-gradient(135deg, #3b82f6, #8b5cf6);">
              {{ post.author?.charAt(0).toUpperCase() }}
            </div>
            <span class="text-xs text-gray-400">{{ post.author }}</span>
          </div>
          <span class="text-xs text-gray-300">{{ formatDate(post.created_at) }}</span>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import api from '../api'

const posts    = ref([])
const filtered = ref([])
const query    = ref('')
const loading  = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const res      = await api.get('/posts/')
    posts.value    = res.data
    filtered.value = res.data
  } finally {
    loading.value = false
  }
})

// Debounce watch — server-side search
let timer
watch(query, (val) => {
  clearTimeout(timer)

  if (!val.trim()) {
    filtered.value = posts.value  // reset ke semua post
    return
  }

  loading.value = true
  timer = setTimeout(async () => {
    try {
      // Hit vuln endpoint → SQLi target
      const res      = await api.get(`/posts/search?q=${val}`)
      filtered.value = res.data.results ?? []
    } catch {
      // Fallback ke client-side kalau endpoint belum ada
      filtered.value = posts.value.filter(p =>
        p.title.toLowerCase().includes(val.toLowerCase()) ||
        p.author.toLowerCase().includes(val.toLowerCase())
      )
    } finally {
      loading.value = false
    }
  }, 400)
})

function clearSearch() {
  query.value    = ''
  filtered.value = posts.value
}

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString('id-ID') : '-'
}
</script>