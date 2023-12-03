<template>
  <div class="wrapper">
    <div class="container content">
      <div class="margin-bottom-20 no-print" style="margin: 20px"></div>
      <div class="row">
        <h1>예금 상품 목록</h1>
        <hr>
        <div class="margin-bottom-30" style="margin: 5px"></div>
        <div class="col-md-12" style="position: relative;">
          <form @submit.prevent="search">
            <label>은행 검색</label>
            <select class="form-control valid" style="width: 300px;" name="bank" id="bank" v-model="selected">
              <option disabled>은행을 선택하세요</option>
              <option value="">전체</option>
              <option v-for="bankname in depoistBanks" :key="bankname">{{ bankname }}</option>
            </select>
          </form>
          <RouterLink v-if="userStore.isLogin === true" class="btn btn-outline-primary" style="position: absolute; bottom: 0px; right: 12px;" :to="{ name: 'deposit_recommend'}">추천 예금 상품</RouterLink>
        </div>
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
                <tr v-for="(deposit, index) in filteredDeposits" :key="deposit.id" @click="goDepositDetail(deposit)">
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
  import { useProductStore } from '@/stores/product'
  import { ref, computed, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useCounterStore } from '@/stores/counter'

  const route = useRoute()
  const router = useRouter()
  const store = useProductStore()
  const userStore = useCounterStore()

  onMounted(() => {
    store.getdeposit()
  })
  
  const depoistBanks = computed(() => {
    const banknames = store.deposit_products.map(product => product.kor_co_nm)
    return Array.from(new Set(banknames))
  })

  const selected = ref('')

  const filteredDeposits = computed(() => {
    if (selected.value) {
      return store.deposit_products.filter(product => product.kor_co_nm === selected.value)
    } else {
      return store.deposit_products
    }
  })

  const search = function () {
    selected.value = selected.value // 검색을 수행하면 selected 값을 갱신
  }

  const getInterestRate = (options, months) => {
    // console.log(options)
    const option = options.find(opt => opt.save_trm === months)
    return option ? option.intr_rate : '-'
  }

  const goDepositDetail = function (deposit) {
    // console.log(deposit)
    router.push({ name: 'depositdetail', params: { deposit_id: deposit.id } })
    console.log('success')
  }

</script>

<style scoped>
  .table {
    width: 90%;
    margin: 25px auto
  }
</style>