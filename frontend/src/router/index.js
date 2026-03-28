import { createRouter, createWebHistory } from 'vue-router'
import LandingView    from '../views/LandingView.vue'
import PostsView      from '../views/PostsView.vue'
import PostView       from '../views/PostView.vue'      
import CreatePostView from '../views/CreatePostView.vue'
import LoginView      from '../views/LoginView.vue'
import RegisterView   from '../views/RegisterView.vue'
import DashboardView  from '../views/DashboardView.vue'
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
  if (to.meta.auth && !token) return next('/login')
  next()
})

export default router