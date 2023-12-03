<template>
  <div class="wrapper">
    <div class="container content" v-if="deposit">
      <div class="margin-bottom-20 no-print" style="margin: 20px"></div>
      <div class="row">
        <h1>예금 상세 페이지</h1>
        <hr>
        <div class="margin-bottom-30" style="margin: 5px"></div>
        <div class="col-md-12" style="position: relative;">
          <div class="btn-group" style="position: absolute; top: 0; right: 140px;">
            <input v-if="!userStore.user.financial_products.includes(deposit.fin_prdt_cd)" class="btn btn-outline-primary" style="margin-right: 20px; display: inline-block;" type="submit" value="가입하기" @click="signup">
            <input v-else class="btn btn-outline-danger" style="margin-right: 20px; display: inline-block;" type="submit" value="가입취소하기" @click="signup">
          </div>
          <div class="btn-group" style="position: absolute; top: 0; right: 0px;">
            <RouterLink type="button" class="btn btn-light" style="margin-right: 20px; display: inline-block;" :to="{ name: 'deposit' }">목록으로 이동</RouterLink>
          </div>
          <div class="table-responsive">
            <table class="table table-borderless" style="width:100%;">
              <thead>
                <tr>
                  <th style="width:15%;">구분</th>
                  <th style="width:85%;">상세</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th>공시 제출월</th>
                  <td>{{ deposit.dcls_month }}</td>
                </tr>
                <tr>
                  <th>금융회사 명</th>
                  <td>{{ deposit.kor_co_nm }}</td>
                </tr>
                <tr>
                  <th>금융 상품명</th>
                  <td>{{ deposit.fin_prdt_nm }}</td>
                </tr>
                <tr>
                  <th>가입 방법</th>
                  <td>{{ deposit.join_way }}</td>
                </tr>
                <tr>
                  <th>만기 후 이자율</th>
                  <td>{{ deposit.mtrt_int }}</td>
                </tr>
                <tr>
                  <th>우대 조건</th>
                  <td>{{ deposit.spcl_cnd }}</td>
                </tr>
                <tr>
                  <th>가입 대상</th>
                  <td>{{ deposit.join_member }}</td>
                </tr>
                <tr>
                  <th>가입 제한</th>
                  <td>{{ join(deposit.join_deny) }}</td>
                </tr>
                <tr>
                  <th>기타 유의사항</th>
                  <td>{{ deposit.etc_note }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import axios from 'axios'
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useProductStore } from '@/stores/product'
  import { useCounterStore } from '@/stores/counter'

  const store = useProductStore()
  const route = useRoute()
  const router = useRouter()
  const depositId = route.params.deposit_id
  const deposit = ref()
  const token = useCounterStore().token
  const userStore = useCounterStore()

  onMounted(() => {
    if (userStore.isLogin === false) {
    alert('로그인이 필요합니다.')
    router.push({ name: 'login' })
  }
    axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/deposits/${depositId}/`,
    })
      .then((res) => {
        // console.log(res.data)
        deposit.value = res.data
        // console.log(deposit.value)
      })
      .catch(err => console.log(err))

    axios({
      method: 'get',
      url: `${store.API_URL}/user/user/`,
      headers: {
        Authorization: `Token ${token}`
      }
    })
      .then((res) => {
        userStore.user.financial_products = res.data.financial_products
      })
      .catch(err => console.log(err))
  })
  
  const join = function (join_deny) {
    if (join_deny === 1) {
      return '제한없음'
    } else if (join_deny === 2) {
      return '서민전용'
    } else if (join_deny === 3) {
      return '일부제한'
    }
  }

  const signup = function () {
    axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/deposits/${depositId}/join/`,
      headers: {
        Authorization: `Token ${token}`
      }
    })
    .then((res) => {
      console.log(store.API_URL,'/api/v1/deposits/',depositId,'/join/')
      console.log('1. res.data.financial_products:', res.data.financial_products)
      userStore.user.financial_products = res.data.financial_products
      console.log('2. userStore.user.financial_products',userStore.user.financial_products)
    })
  }
</script>

<style scoped>

</style>