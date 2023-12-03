// import axios from 'axios'
// import { computed, ref } from 'vue'
// import { defineStore } from 'pinia'
// import { useCounterStore } from '@/stores/counter'

// export const useAuthStore = defineStore('auth', () => {
//   const API_URL = 'http://127.0.0.1:8000'
//   const user = ref('')
//   const token = useCounterStore().token

//   const getUserInfo = function () {
//     console.log(1, token)
//     axios({
//       method: 'get',
//       url: `${API_URL}/user/user`,
//       headers:{
//         Authorization: `Token ${token}`
//       }
//     })
//     .then((res) => {
//       user.value = res.data
//       console.log(0, user.value)
      
//     })
//     .catch(err => console.log(err))
//   }
//   return { API_URL, user, getUserInfo }
//   })