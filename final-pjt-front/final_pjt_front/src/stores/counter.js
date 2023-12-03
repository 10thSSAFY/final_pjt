import axios from 'axios'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const router = useRouter()
  const token = ref(null)
  const API_URL = `http://127.0.0.1:8000`
  // const auth = useAuthStore()
  const user = ref('')
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })

  const signUp = function (signupPayload) {
    const { username, email, password1, password2} = signupPayload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, email, password1, password2
      }
    })
    .then((res) => {
      console.log(res)
      console.log('회원가입 완료')
      alert('회원가입을 환영합니다.')
      const password = password1
      logIn({ username, password })
      // router.push({ name: 'home' })
    })
    .catch(err => console.log(err))
  }

  const logIn = function (loginPayload) {
    const { username, password } = loginPayload
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, 
        password,
      }
    })
    .then((res) => {
      console.log(res.data)
      console.log('로그인 완료')
      token.value = res.data.key
      // console.log(0, token)
      // auth.getUserInfo()      
      axios({
        method: 'get',
        url: `${API_URL}/user/user`,
        headers:{
          Authorization: `Token ${token.value}`
        }
      }) 
      .then((res) => {
        // console.log(111, res)
        user.value = res.data
        router.push({ name: 'home' })
        // console.log(0, user.value)
      })
    })
    .catch(err => console.log(err))
  }

  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
    })
    .then((res) => {
      token.value = null
      user.value = null
      localStorage.removeItem('user')
      localStorage.removeItem('token')
      sessionStorage.removeItem('user')
      sessionStorage.removeItem('token')
      router.push({ name: 'home' })
    })
    .catch(err => console.log(err))
  }
  return { router, token, API_URL, signUp, logIn, logOut, isLogin, user }
}, { persist: true })
