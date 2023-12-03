import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import PostView from '@/views/Post/PostView.vue'
import PostDetailView from '@/views/Post/PostDetailView.vue'
import ExchangeRateView from '@/views/ExchangeRateView.vue'

import DepositListView from '@/views/Product/DepositListView.vue'
import DepositListDetailView from '@/views/Product/DepositListDetailView.vue'
import DepositListRecommend from '@/views/Product/DepositListRecommend.vue' 
import SaveListView from '@/views/Product/SaveListView.vue'
import SaveListDetailView from '@/views/Product/SaveListDetailView.vue'
import SaveListRecommend from '@/views/Product/SaveListRecommend.vue' 

import SignUpView from '@/views/Auth/SignUpview.vue'
import LoginView from '@/views/Auth/LoginView.vue'
import SearchBankView from '@/views/SearchBankView.vue'
import CategoryCreateView from '@/views/Post/CategoryCreateView.vue'
import PostCreateView from '@/views/Post/PostCreateView.vue'
import PostUpdateView from '@/views/Post/PostUpdateView.vue'
import ProfilView from '@/views/Auth/ProfilView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/post',
      name: 'post',
      component: PostView
    },
    {
      path: '/createpost',
      name: 'createpost',
      component: PostCreateView
    },
    {
      path: '/post/:post_id',
      name: 'postdetail',
      component: PostDetailView
    },
    {
      path: '/update/:post_id',
      name: 'postupdate',
      component: PostUpdateView
    },
    {
      path: '/exchange',
      name: 'exchange',
      component: ExchangeRateView
    },
    {
      path: '/deposit',
      name: 'deposit',
      component: DepositListView
    },
    {
      path: '/deposit/:deposit_id',
      name: 'depositdetail',
      component: DepositListDetailView
    },
    {
      path: '/save',
      name: 'savelist',
      component: SaveListView
    },
    {
      path: '/save/:save_id',
      name: 'savelistdetail',
      component: SaveListDetailView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchBankView
    },
    {
      path: '/category',
      name: 'category',
      component: CategoryCreateView
    },
    {
      path: '/user',
      name: 'user',
      component: ProfilView
    },
    {
      path: '/deposit/recommend',
      name: 'deposit_recommend',
      component: DepositListRecommend
    },
    {
      path: '/save/recommend',
      name: 'save_recommend',
      component: SaveListRecommend
    }
  ]
})

export default router
