<template>
  <nav class="sticky top-0 z-50 border-b border-white/20"
       style="background: rgba(255,255,255,0.72); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);">
    <div class="max-w-5xl mx-auto px-6 h-14 flex items-center justify-between">

      <!-- Logo -->
      <RouterLink to="/"
        class="font-bold text-lg tracking-tight"
        style="color: #1d6ef5;">
        VulnBlog
      </RouterLink>

      <!-- Nav Links -->
      <div class="flex items-center gap-1">
        <RouterLink to="/posts"
          class="px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200"
          style="color: #374151;"
          active-class="!text-blue-600 bg-blue-50/80">
          Posts
        </RouterLink>

        <!-- Sudah login -->
        <template v-if="auth.isLoggedIn">
          <RouterLink to="/dashboard"
            class="px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200"
            style="color: #374151;"
            active-class="!text-blue-600 bg-blue-50/80">
            Dashboard
          </RouterLink>

          <RouterLink to="/create"
            class="ml-1 px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all duration-200 border"
            style="
              background: rgba(59,130,246,0.12);
              color: #2563eb;
              border-color: rgba(59,130,246,0.25);
            "
            onmouseover="this.style.background='rgba(59,130,246,0.2)'"
            onmouseout="this.style.background='rgba(59,130,246,0.12)'">
            + Post
          </RouterLink>

          <!-- User pill -->
          <div class="ml-2 flex items-center gap-2 px-3 py-1 rounded-full border"
               style="
                 background: rgba(243,244,246,0.6);
                 border-color: rgba(209,213,219,0.5);
               ">
            <!-- Avatar inisial -->
            <div class="w-5 h-5 rounded-full flex items-center justify-center text-xs font-semibold text-white"
                 style="background: linear-gradient(135deg, #3b82f6, #8b5cf6);">
              {{ auth.user?.username?.charAt(0).toUpperCase() }}
            </div>
            <span class="text-sm font-medium" style="color: #374151;">
              {{ auth.user?.username }}
            </span>
            <button @click="doLogout"
              class="text-xs font-medium transition-colors duration-200 ml-1"
              style="color: #9ca3af;"
              onmouseover="this.style.color='#ef4444'"
              onmouseout="this.style.color='#9ca3af'">
              Logout
            </button>
          </div>
        </template>

        <!-- Belum login -->
        <template v-else>
          <RouterLink to="/login"
            class="px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200"
            style="color: #374151;"
            active-class="!text-blue-600">
            Login
          </RouterLink>
          <RouterLink to="/register"
            class="ml-1 px-3.5 py-1.5 rounded-lg text-sm font-medium border transition-all duration-200"
            style="
              background: rgba(59,130,246,0.12);
              color: #2563eb;
              border-color: rgba(59,130,246,0.25);
            "
            onmouseover="this.style.background='rgba(59,130,246,0.2)'"
            onmouseout="this.style.background='rgba(59,130,246,0.12)'">
            Register
          </RouterLink>
        </template>
      </div>

    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const auth   = useAuthStore()
const router = useRouter()

function doLogout() {
  auth.logout()
  router.push('/')
}
</script>