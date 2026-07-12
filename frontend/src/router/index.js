import { createRouter, createWebHistory } from 'vue-router'
import LandingView    from '../views/LandingView.vue'
import PostsView      from '../views/PostsView.vue'
import PostView       from '../views/PostView.vue'
import CreatePostView from '../views/CreatePostView.vue'
import LoginView      from '../views/LoginView.vue'
import RegisterView   from '../views/RegisterView.vue'
import DashboardView  from '../views/DashboardView.vue'
import AdminView      from '../views/AdminView.vue'
import MainLayout     from '../layouts/MainLayout.vue'

const routes = [
  { path: '/', component: LandingView },
  {
    path: '/',
    component: MainLayout,
    children: [
      { path: 'posts',     component: PostsView },
      { path: 'post/:id',  component: PostView },
      { path: 'create',    component: CreatePostView, meta: { auth: true } },
      { path: 'dashboard', component: DashboardView,  meta: { auth: true } },
      { path: 'admin',     component: AdminView,      meta: { auth: true, admin: true } },
      { path: 'login',     component: LoginView },
      { path: 'register',  component: RegisterView },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const user  = JSON.parse(localStorage.getItem('user') || 'null')

  if (to.meta.auth && !token) return next('/login')
  if (to.meta.admin && user?.role !== 'admin') return next('/dashboard')
  next()
})

export default router