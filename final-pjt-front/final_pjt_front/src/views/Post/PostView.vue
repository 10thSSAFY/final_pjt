<template>
  <div class="wrapper">
    <div class="container content">
      <div class="margin-bottom-20 no-print" style="margin: 20px"></div>
      <div class="row">
        <h1>게시판 페이지</h1>
        <div class="col-md-12">
          <ul class="nav nav-pills">
            <RouterLink :to="{ name: 'home' }" tag="button" type="button" class="btn btn-outline-primary" id="link" style="margin: 0px 2px;">홈으로</RouterLink>
            <RouterLink :to="{ name: 'createpost' }" tag="button" type="button" class="btn btn-outline-primary" id="link" style="margin: 0px 2px;">게시글 생성</RouterLink>
            <RouterLink :to="{ name: 'category' }" tag="button" type="button" class="btn btn-outline-danger" id="link" v-if="userStore.user && userStore.user.is_superuser === true" style="margin: 0px 2px;">카테고리 생성</RouterLink>
          </ul>
          <div style="margin: 25px 0px -10px;">
            <select class="form-control valid" style="width: 250px;" v-model="selectedCategory">
              <option value="">모든 카테고리</option>
              <option v-for="category in categories" :key="category">{{ category }}</option>
            </select>
          </div>
        </div>
        <div class="margin-bottom-30"></div>
        <div class="col-md-12">
          <div class="table-responsive">
            <table class="table table-bordered table-striped" style="width:100%;">
              <thead>
                <tr>
                  <th style="width:5%;">번호</th>
                  <th style="width:12%;">카테고리</th>
                  <th style="width:49%;">제목</th>
                  <th style="width:14%;">작성자</th>
                  <th style="width:20%;">등록시간</th>
                </tr>
              </thead>
              <tbody>
                <!-- <tr v-for="(post, index) in store.posts" @click="goDetail(post)" :key="index"> -->
                <tr v-for="(post, index) in filteredCategories" @click="goDetail(post)" :key="index">
                  <th scope="row">{{ index+1 }}</th>
                  <td>{{ post.category.name }}</td>
                  <td>{{ post.title }}</td>
                  <td>{{ post.user.username }}</td>
                  <td>{{ formatDate(post.created_at) }}</td>
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
import { RouterLink } from "vue-router";
import { usePostStore } from "@/stores/post";
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { useCounterStore } from "@/stores/counter"

const userStore = useCounterStore()
const store = usePostStore();

onMounted(() => {
  store.getPosts();
  if (userStore.isLogin === false) {
    alert('로그인이 필요합니다.')
    router.push({ name: 'login' })
  }
});

const selectedCategory = ref('')

onMounted(() => {
  store.getCategory()
})

const categories = computed(() => {
  const categorynames = store.category.map(category => category.name)
  return Array.from(new Set(categorynames))
})

const filteredCategories = computed(() => {
  if (selectedCategory.value) {
    return store.posts.filter(post => post.category.name === selectedCategory.value)
  } else {
    return store.posts
  }
})

const router = useRouter();
const goDetail = function (post) {
  router.push({ name: "postdetail", params: { post_id: post.id } });
};

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const formattedDate = date.toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' })
  return formattedDate
}
</script>

<style scoped>
.table {
  width: 90%;
  margin: 25px auto;
}
#link {
  text-decoration: none;
}
</style>
