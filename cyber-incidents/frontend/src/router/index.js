import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import IncidentsView from '../views/IncidentsView.vue'
import RegisterView from '../views/RegisterView.vue'

const routes = [
  {
    path: '/',
    name: 'login',
    component: LoginView
  },
  {
    path: '/login',
    redirect: '/' // Добавляем редирект
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/incidents',
    name: 'incidents',
    component: IncidentsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*', // Ловим все несуществующие пути
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Проверка авторизации
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('auth')
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router