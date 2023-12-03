<template>
  <div>
    <h1>카테고리 생성</h1>
    <form @submit.prevent="createCategory">
      <label for="name">Category 종류:</label>
      <input type="text" id="name" v-model="name">
      <input type="submit" value="카테고리 생성">
    </form>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  import { usePostStore } from '@/stores/post'
  import { useRouter } from 'vue-router'


  const name = ref('')
  const store = usePostStore()
  const router = useRouter()

  const createCategory = function () {
    axios({
      method: 'post',
      url: `${store.API_URL}/api/v1/category/`,
      data: {
        name: name.value
      },
    })
    .then(() => {
      router.push({ name:'post' })
    })
    .catch(err => console.log(err))
  }
</script>

<style scoped>

</style>