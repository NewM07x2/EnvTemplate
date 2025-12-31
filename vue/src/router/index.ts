import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import GraphQLPage from '@/views/GraphQLPage.vue'
import PrismaPage from '@/views/PrismaPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/graphql',
      name: 'graphql',
      component: GraphQLPage
    },
    {
      path: '/prisma',
      name: 'prisma',
      component: PrismaPage
    }
  ]
})

export default router
