<template>
  <div class="d-flex flex-column vh-100 justify-content-start align-items-center">
    <div class="btn-group d-flex flex-wrap justify-content-center mb-5" role="group" aria-label="Basic radio toggle button group">
      <div class="me-2" v-for="(saveTrm, index) in saveTrms" :key="'save'+index">
        <input type="radio" class="btn-check" name="btnradio" :id="'btnradio'+index" @click="createChart(saveTrm, 'save')" autocomplete="off">
        <label class="btn btn-outline-primary" :for="'btnradio'+index">{{ saveTrm }}개월 (적금)</label>
      </div>
      <div class="me-2" v-for="(saveTrm, index) in depositTrms" :key="'deposit'+index">
        <input type="radio" class="btn-check" name="btnradio" :id="'btnradio'+(index+saveTrms.length)" @click="createChart(saveTrm, 'deposit')" autocomplete="off">
        <label class="btn btn-outline-primary" :for="'btnradio'+(index+saveTrms.length)">{{ saveTrm }}개월 (예금)</label>
      </div>
    </div>
    <canvas id="chart"></canvas>
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import { Chart, registerables } from 'chart.js';
import axios from "axios";
import { useCounterStore} from "@/stores/counter";

Chart.register(...registerables)
const store = useCounterStore()

const userInfo = ref(null);
const saveTrms = ref([]);
const depositTrms = ref([]);
const allData = ref({});
let myChart = null

onMounted(async () => {
  const token = useCounterStore().token;
  await axios({
    method: 'get',
    url:`${store.API_URL}/api/v1/join_info/`,
    headers: {
      Authorization: `Token ${token}`
    }
  })
  .then((response) => {
    userInfo.value = response.data;
    response.data.forEach(item => {
      if (item.saveoptionlist_set && item.saveoptionlist_set.length > 0) {
        item.saveoptionlist_set.forEach(option => {
          const { save_trm, intr_rate, intr_rate2 } = option;
          if (!saveTrms.value.includes(save_trm)) {
            saveTrms.value.push(save_trm);
          }
          if (!allData.value[save_trm]) {
            allData.value[save_trm] = {
              save: {
                labels: [],
                intr_rate: [],
                intr_rate2: []
              },
              deposit: {
                labels: [],
                intr_rate: [],
                intr_rate2: []
              }
            };
          }
          allData.value[save_trm].save.labels.push(item.fin_prdt_nm);
          allData.value[save_trm].save.intr_rate.push(intr_rate);
          allData.value[save_trm].save.intr_rate2.push(intr_rate2);
        });
      }
      if (item.depositoptionlist_set && item.depositoptionlist_set.length > 0) {
        item.depositoptionlist_set.forEach(option => {
          const { save_trm, intr_rate, intr_rate2 } = option;
          if (!depositTrms.value.includes(save_trm)) {
            depositTrms.value.push(save_trm);
          }
          if (!allData.value[save_trm]) {
            allData.value[save_trm] = {
              save: {
                labels: [],
                intr_rate: [],
                intr_rate2: []
              },
              deposit: {
                labels: [],
                intr_rate: [],
                intr_rate2: []
              }
            };
          }
          allData.value[save_trm].deposit.labels.push(item.fin_prdt_nm);
          allData.value[save_trm].deposit.intr_rate.push(intr_rate);
          allData.value[save_trm].deposit.intr_rate2.push(intr_rate2);
        });
      }
    });
  });
});

const createChart = (saveTrm, type) => {
  const ctx = document.getElementById('chart').getContext('2d');

  if (myChart) {
    myChart.destroy();
  }

  myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: allData.value[saveTrm][type].labels,
      datasets: [
        {
          label: `${saveTrm}개월 ${type === 'save' ? '저축' : '예금'} 금리`,
          data: allData.value[saveTrm][type].intr_rate,
          backgroundColor: 'rgba(75, 192, 192, 0.5)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        },
        {
          label: `${saveTrm}개월 ${type === 'save' ? '저축' : '예금'} 최고 우대금리`,
          data: allData.value[saveTrm][type].intr_rate2,
          backgroundColor: 'rgba(153, 102, 255, 0.5)',
          borderColor: 'rgba(153, 102, 255, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
};
</script>