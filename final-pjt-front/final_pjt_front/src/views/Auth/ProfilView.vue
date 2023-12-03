<template>
  <div class="wrapper">
    <div class="container content">
      <div class="margin-bottom-20 no-print" style="margin: 20px"></div>
      <div class="row">
        <div class="text-center">
          <h1>유저 정보 페이지</h1>
        </div>
        <hr>
        <div class="margin-bottom-30" style="margin: 5px"></div>
        <div class="col-md-12" style="margin: 0px 20%;">
          <div class="table-responsive" v-if="store.user">
            <table class="table table-borderless" style="width:100%;">
              <thead style="display:none;">
                <tr>
                  <th style="width:17%;"></th>
                  <th style="width:28%;"></th>
                  <th style="width:55%;"></th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th>아이디</th>
                  <td>{{ store.user.username }}</td>
                  <td></td>
                </tr>
                <tr>
                  <th>이메일</th>
                  <td>{{ store.user.email }}</td>
                </tr>
                <tr>
                  <th>가입일</th>
                  <td>{{ formatDate(store.user.date_joined) }}</td>
                </tr>
                <tr>
                  <th>나이</th>
                  <td>{{ age }}</td>
                  <td>
                    <form class="row g-3 align-items-center" @submit.prevent="updateage">
                      <div class="col-auto">
                        <input type="number" class="form-control" style="width:5em;" v-model="age" />
                      </div>
                      <div class="col-auto">
                        <input type="submit" value="저장" />
                      </div>
                    </form>
                  </td>
                </tr>
                <tr>
                  <th>희망 저축 기간</th>
                  <td>{{ style }}개월</td>
                  <td>
                    <form class="row g-3 align-items-center" @submit.prevent="updateSavetrm">
                      <div class="col-auto">
                        <select class="form-control" style="width:5em;" name="style" id="style" v-model="select">
                          <option value="6">6개월</option>
                          <option value="12">12개월</option>
                          <option value="24">24개월</option>
                          <option value="36">36개월</option>
                        </select>
                      </div>
                      <div class="col-auto">
                        <input type="submit" value="저장" />
                      </div>
                    </form>
                  </td>
                </tr>
                <tr>
                  <th>선호 은행</th>
                  <td>{{ bank }}</td>
                  <td>
                    <!-- <form class="row g-3 align-items-center" @submit.prevent="updatebank">
                      <div class="col-auto">
                        <input class="form-control" style="width:10em;" type="text" v-model="bank" :placeholder="store.user.maninbank" />
                      </div>
                      <div class="col-auto">
                        <input type="submit" value="저장" />
                      </div>
                    </form> -->
                    <form class="row g-3 align-items-center" @submit.prevent="updatebank">
                      <div class="col-auto">
                        <select class="form-control" style="width:10em;" name="style" id="style" v-model="bank">
                          <option disabled>은행을 선택하세요</option>
                          <option v-for="bankname in Banksname" :key="bankname">{{ bankname }}</option>
                        </select>
                      </div>
                      <div class="col-auto">
                        <input type="submit" value="저장" />
                      </div>
                    </form>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <hr>
        <div class="col-md-12">
          <div class="text-center" style="margin: 5px 0px;">
            <h3>가입한 상품</h3>
            <RouterLink class="btn btn-outline-primary" style="margin: 0px 5px;" :to="{ name: 'deposit_recommend'}">추천 예금 상품</RouterLink>
            <RouterLink class="btn btn-outline-primary" style="margin: 0px 5px;" :to="{ name: 'save_recommend'}">추천 적금 상품</RouterLink>
          </div>
          <div style="margin: 40px 10px;">
            <span v-for="signup in signupInfo" id="info">
              <div class="alert alert-warning text-center" role="alert" style="margin: -5px 20%;">{{ signup.fin_prdt_nm }}</div>
              <br>
            </span>
          </div>
        </div>
        <hr>
        <div class="col-md-12">
          <div class="text-center" style="margin: 5px 0px;">
            <h3>가입 상품 금리 비교</h3>
          </div>
          <Chart />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted, watchEffect, computed } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useProductStore } from '@/stores/product'
import Chart from '@/components/Chart.vue'

const bank = ref("");
const age = ref("");
const store = useCounterStore();
const token = useCounterStore().token;
const signupInfo = ref();
const select = ref("");
const style = ref("");
const productstore = useProductStore()

const saveBanks = computed(() => {
    const banknames = productstore.save_products.map(product => product.kor_co_nm)
    return Array.from(new Set(banknames))
  })

const depoistBanks = computed(() => {
  const banknames = productstore.deposit_products.map(product => product.kor_co_nm)
  return Array.from(new Set(banknames))
})

const Banksname = computed(() => {
  const savenames = saveBanks.value
  const depositnames = depoistBanks.value
  const combined = [...savenames, ...depositnames]
  const banknames = Array.from(new Set(combined))
  return banknames
})

onMounted(() => {
  productstore.getdeposit()
  productstore.getsave()
  axios({
    method: `get`,
    url: `${store.API_URL}/user/user/`,
    headers: {
      Authorization: `Token ${token}`,
    },
  }).then((res) => {
    console.log(res.data);
    age.value = res.data.age;
    bank.value = res.data.maninbank;
    style.value = res.data.savestyle;
    axios({
      method: "get",
      url: `${store.API_URL}/api/v1/join_info/`,
      headers: {
        Authorization: `Token ${token}`,
      },
    }).then((res) => {
      console.log(res.data);
      signupInfo.value = res.data;
    });
  });
});

watchEffect(() => {
  if (store.user.age) {
    age.value = store.user.age;
  }
});

watchEffect(() => {
  if (store.user.maninbank) {
    bank.value = store.user.maninbank;
  }
});

watchEffect(() => {
  if (store.user.savestyle) {
    style.value = store.user.savestyle;
  }
});

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const formattedDate = date.toLocaleString("ko-KR", {
    timeZone: "Asia/Seoul",
  });
  return formattedDate;
};

const updatebank = function () {
  axios({
    method: "put",
    url: `${store.API_URL}/user/user/`,
    data: {
      maninbank: bank.value,
    },
    headers: {
      Authorization: `Token ${token}`,
    },
  })
    .then((res) => {
      console.log(res.data.maninbank);
      // store.user.maninbank = (res.data.maninbank)
      // bank.value = ''
    })
    .catch((err) => console.log(err));
};

const updateage = function () {
  axios({
    method: "put",
    url: `${store.API_URL}/user/user/`,
    data: {
      age: age.value,
    },
    headers: {
      Authorization: `Token ${token}`,
    },
  })
    .then((res) => {
      console.log(res.data.age);
    })
    .catch((err) => console.log(err));
};

const updateSavetrm = function () {
  axios({
    method: "put",
    url: `${store.API_URL}/user/user/`,
    data: {
      savestyle: select.value,
    },
    headers: {
      Authorization: `Token ${token}`,
    },
  })
    .then((res) => {
      console.log(res.data.savestyle);
      style.value = res.data.savestyle;
    })
    .catch((err) => console.log(err));
};
</script>

<style scoped>
.table tr {
  height: 55px;
}
.table td, .table th {
  vertical-align: middle;
}
</style>
