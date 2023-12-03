<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="http://localhost:5173/">DayBank</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <RouterLink :to="{ name: 'home' }" class="nav-link active" aria-current="page">홈</RouterLink>
            </li>
            <li class="nav-item">
              <a class="nav-link active" href="http://localhost:5173/post">게시판</a>
              <!-- <RouterLink :to="{ name: 'post' }" class="nav-link active" aria-current="page">게시판</RouterLink> -->
            </li>
            <li class="nav-item">
              <RouterLink :to="{ name: 'exchange' }" class="nav-link active" aria-current="page">환율</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink :to="{ name: 'search' }" class="nav-link active" aria-current="page">가까운 은행찾기</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink :to="{ name: 'deposit' }" class="nav-link active" aria-current="page">예금</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink :to="{ name: 'savelist' }" class="nav-link active" aria-current="page">적금</RouterLink>
            </li>
          </ul>
          <ul class="navbar-nav ms-auto">
            <li v-if="store.isLogin" class="nav-item">
              <form @submit.prevent="store.logOut">
                <input type="submit" value="로그아웃" class="nav-link active" aria-current="page">
              </form>
            </li>
            <li v-if="store.isLogin" class="nav-item">
              <RouterLink :to="{ name: 'user' }" class="nav-link active" aria-current="page">프로필</RouterLink>
            </li>
            <li v-if="!store.isLogin" class="nav-item">
              <RouterLink :to="{ name: 'signup' }" class="nav-link active" aria-current="page">회원가입</RouterLink>
            </li>
            <li v-if="!store.isLogin" class="nav-item">
              <RouterLink :to="{ name: 'login' }" class="nav-link active" aria-current="page">로그인</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
  <RouterView />
</template>


<script setup>
  import { useCounterStore } from '@/stores/counter'
  import { RouterView, RouterLink } from 'vue-router'
  import { useProductStore } from '@/stores/product'
  import { onMounted } from 'vue'
  
  const store = useCounterStore()
  const store1 = useProductStore()
  onMounted(() => {
    store1.loadDepoistProducts()
  })
</script>

<style scoped>

</style>
