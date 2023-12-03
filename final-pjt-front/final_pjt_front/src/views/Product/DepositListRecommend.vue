<template>
  <div class="wrapper">
    <div class="container content">
      <div class="margin-bottom-20 no-print" style="margin: 20px"></div>
      <div class="row">
        <h1>추천 예금 상품</h1>
        <hr>
        <div class="col-md-12">
          <div class="table-responsive">
            <table class="table table-bordered table-striped" style="width:100%;">
              <thead>
                <tr>
                  <th style="width:5%;"></th>
                  <th style="width:10%;">공시제출월</th>
                  <th style="width:18%;">은행명</th>
                  <th style="width:39%;">상품명</th>
                  <th style="width:7%;">6개월</th>
                  <th style="width:7%;">12개월</th>
                  <th style="width:7%;">24개월</th>
                  <th style="width:7%;">36개월</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(deposit, index) in depositRecommend" :key="deposit.id" @click="goDepositDetail(deposit)">
                  <th scope="row">{{ index + 1 }}</th>
                  <td>{{ deposit.dcls_month }}</td>
                  <td>{{ deposit.kor_co_nm }}</td>
                  <td>{{ deposit.fin_prdt_nm }}</td>
                  <td>{{ getInterestRate(deposit.depositoptionlist_set, 6) }}</td>
                  <td>{{ getInterestRate(deposit.depositoptionlist_set, 12) }}</td>
                  <td>{{ getInterestRate(deposit.depositoptionlist_set, 24) }}</td>
                  <td>{{ getInterestRate(deposit.depositoptionlist_set, 36) }}</td>
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
import { useProductStore } from '@/stores/product'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const store = useProductStore()
const token = useCounterStore().token
const depositRecommend = ref()
const router = useRouter()

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/deposits/recommend/`,
    headers: {
      Authorization: `Token ${token}`
    }
  })
    .then((res) => {
      console.log(res.data)
      depositRecommend.value = res.data
    })
    .catch(err => console.log(err))
})

const getInterestRate = (options, months) => {
  const option = options.find(opt => opt.save_trm === months)
  return option ? option.intr_rate : '-'
}

const goDepositDetail = function (deposit) {
  router.push({ name: 'depositdetail', params: { deposit_id: deposit.id } })
}
</script>

<style scoped>

</style>