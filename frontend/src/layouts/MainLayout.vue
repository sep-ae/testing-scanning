<template>
  <div class="min-h-screen"
       style="background: linear-gradient(135deg, #f0f4ff 0%, #faf5ff 50%, #f0fdf4 100%);">
    <Navbar />
    <main class="max-w-5xl mx-auto px-6 py-8">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
</script>