import axios from 'axios'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

export const useProductStore = defineStore('product', () => {
  const deposit_products = ref([])
  const save_products = ref([])
  const API_URL = 'http://127.0.0.1:8000'

  const loadDepoistProducts = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/save-deposit-products/`
    })
    .then((res) => {
      console.log('okay')
    })
  }
  const getdeposit = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/deposits/`,
    })
    .then((res) => {
      // console.log(res.data)
      deposit_products.value = res.data
      console.log('okay')
    })
    .catch(err => console.log(err))
  }

  const getsave = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/saves/`,
    })
    .then((res) => {
      // console.log(res.data)
      save_products.value = res.data
      console.log('okay')
    })
  }
  
  return { deposit_products, save_products, API_URL, loadDepoistProducts, getdeposit, getsave }
})