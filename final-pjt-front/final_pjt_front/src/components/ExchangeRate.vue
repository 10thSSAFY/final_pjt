<template>
  <div class="wrapper">
    <div class="container content">
      <div class="margin-bottom-20 no-print" style="margin: 20px;"></div>
      <div class="row">
        <div class="col-md-12">
          <h1>환율 정보 검색</h1>
          <hr>
          <form class="form-horizontal">
            <div class="form-group">
              <div class="col-md-2">
                <select class="form-control valid" v-model="selectCurrency">
                  <option v-for="exchangerate in store.exchangerates" :value="exchangerate">{{ exchangerate.cur_nm }}</option>
                </select>
              </div>
            </div>
            <div class="form-group" style="margin: 10px 0px;">
              <div class="col-md-4 d-flex align-items-center">
                <input class="form-control" type="text" id="won" v-model="from_won" @input="calculateExchange1">
                <label for="won" style="width: 500px; margin: 0px 5px;">한국 원</label>
              </div>
              <p>{{ to_dollar }} {{ selectCurrency ? selectCurrency.cur_nm : '' }}</p>
            </div>
            <div class="form-group">
              <div class="col-md-4 d-flex align-items-center">
                <input class="form-control" type="text" id="dollar" v-model="from_dollar" @input="calculateExchange2">
                <label for="dollar" style="width: 500px; margin: 0px 5px;">{{ selectCurrency ? selectCurrency.cur_nm : '' }}</label>
              </div>
              <p>{{ to_won }} 한국 원</p>
            </div>
            <p>* 엔화, 인도네시아 루피아는 100단위, 나머지는 모두 1단위</p>
          </form>
        </div>
        <div class="col-md-12 detail">

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useExchangeStore } from '@/stores/exchange.js'

const selectCurrency = ref(null)
const from_won = ref('')
const to_dollar = ref('0.00') 
const from_dollar = ref('')
const to_won = ref('0.00')
const store = useExchangeStore()

onMounted(async () => {
  await store.getExchange()
})
watch(() => store.exchangerates, (newVal) => {
  if(newVal.length > 0){
    selectCurrency.value = newVal[0]
  }
}, { immediate: true })
// selectCurrency 값이 변경될 때마다 to_dollar와 to_won 값을 0.00으로 초기화합니다.
watch(selectCurrency, () => {
  to_dollar.value = '0.00'
  to_won.value = '0.00'
  from_dollar.value = ''
  from_won.value = ''
})

const cur_nm = ref(null)
const deal_bas_r = ref(null)
const ttb = ref(null)
const tts = ref(null)
const exchange_result = ref(null)

const calculateExchange1 = function () {
  tts.value = String(selectCurrency.value.tts)
  const ttsAsNumber = parseFloat(tts.value.replace(',', ''))
  exchange_result.value = (from_won.value/ttsAsNumber)
  to_dollar.value = exchange_result.value.toFixed(2)
}

const calculateExchange2 = function () {
  ttb.value = String(selectCurrency.value.ttb)
  const ttbAsNumber = parseFloat(tts.value.replace(',', ''))
  exchange_result.value = (from_dollar.value*ttbAsNumber)
  to_won.value = exchange_result.value.toFixed(2)
}
</script>

<style scoped>

</style>