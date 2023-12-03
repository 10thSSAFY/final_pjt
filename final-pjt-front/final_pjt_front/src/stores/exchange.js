import axios from 'axios'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'

export const useExchangeStore = defineStore('exchange', () => {
  const exchangerates = ref([])
  const getExchange = function() {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/exchanges/`
    })
      .then(res => {
        console.log(res)
        exchangerates.value = res.data
      })
      .catch(err => console.log(err))
  }
  return { getExchange, exchangerates }
})