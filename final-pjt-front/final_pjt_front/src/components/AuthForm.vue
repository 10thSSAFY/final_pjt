<template>
  <div class="form-card">

    <div v-if="route.name === 'signup'">
      <h1>회원가입</h1>
      <form class="signup-form" @submit.prevent="sighUp">
        <label for="username">아이디</label>
        <input type="text" id="username" v-model.trim="username">

        <label for="nickname">닉네임</label>
        <input type="text" id="nickname" v-model.trim="nickname">

        <label for="email">이메일</label>
        <input type="email" id="email" v-model.trim="email" placeholder="abc@gmail.com">

        <label for="password1">비밀번호</label>
        <input type="password" id="password1" v-model.trim="password1">

        <label for="password2">비밀번호 재확인</label>
        <input type="password" id="password2" v-model.trim="password2">

        <input type="submit" class="signup-submit-btn" value="가입하기">
      </form>
    </div>

    <div v-if="route.name === 'login'">
      <h1>로그인</h1>
      <form class="login-form" @submit.prevent="logIn">
        <label for="username">아이디</label>
        <input type="text" id="username" v-model.trim="username">

        <label for="password1">비밀번호</label>
        <input type="password" id="password1" v-model.trim="password">

        <input type="submit" class="login-submit-btn" value="로그인">
      </form>
    </div>
    
  </div>
</template>
  
<script setup>
  import { ref } from 'vue'
  import { useRoute } from 'vue-router'
  import { useCounterStore } from '@/stores/counter'

  const store = useCounterStore()
  const route = useRoute()

  const username = ref(null)
  const nickname = ref(null)
  const email = ref(null)
  const password1 = ref(null)
  const password2 = ref(null)
  const password = ref(null)

  const sighUp = function () {
    const signupPayload = {
      username: username.value,
      nickname: nickname.value,
      email: email.value,
      password1: password1.value,
      password2: password2.value
    }
    store.signUp(signupPayload)
  }

  const logIn = function () {
    const loginPayload = {
      username: username.value,
      password: password.value
    }
    store.logIn(loginPayload)
  }
</script>

<style scoped>
  .form-card {
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    border: 1px black solid;
    margin: 20px auto;
    width: 70%;
  }

  h1{
    text-align: center;
    background-color: #F8F4B9;
    padding: 5px;
  }

  .signup-form{
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    padding: 10px;
  }

  .login-form{
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    padding: 10px;
  }
  .signup-submit-btn{
    margin-top: 20px;
    background-color: #B9DDF8;
    border: 0px;
    border-radius: 3%;
  }

  .login-submit-btn{
    margin-top: 50px;
    background-color: #B9DDF8;
    border: 0px;
    border-radius: 3%;
  }
</style>