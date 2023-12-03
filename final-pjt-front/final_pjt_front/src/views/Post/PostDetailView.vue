<template>
  <div class="wrapper">
    <div class="container content">
      <div class="margin-bottom-20 no-print" style="margin: 20px;"></div>
      <div class="row" v-if="post">
        <div class="col-md-12">
          <h3>게시글 상세 정보</h3>
          <hr>
        </div>
        <div class="col-md-12">
          <div class="page-header d-flex justify-content-between" style="margin: -10px 30px -10px;">
            <span id="category">{{ post.category.name }}</span>
            <span>{{ username }}&nbsp;&nbsp;|&nbsp;&nbsp;{{ post.updated_at }}</span>
          </div>
          <hr>
        </div>
        <div class="col-md-12 comment">
          <div class="panel panel-default">
            <div class="panel-heading">
              <h6 class="panel-title">
                <h1>{{ post.title }}</h1>
              </h6>
            </div>
            <div class="panel-body">
              <div class="content post" style="line-height:30px; padding: 0px 20px;">{{ post.content }}</div>
            </div>
            <hr>
            <div v-if="username === userStore.user.username">
              <input class="btn btn-outline-primary" type="submit" value="수정" style="margin: 0px 2px;" @click="updatePost(post)" :post="post"/>
              <input class="btn btn-outline-danger" type="submit" value="삭제" style="margin: 0px 2px;" @click="deletePost(post.id)" />
              <hr>
            </div>
          </div>
        </div>
        <div class="col-md-12">
          <form @submit.prevent="createComment" style="border: lightgray 1px solid; padding: 20px; border-radius:9px;">
            <h5 style="margin: 5px 2px;">댓글 작성</h5>
            <input class="form-control" type="text" v-model.trim="content" />
            <input class="btn btn-outline-primary" type="submit" value="등록" style="margin: 5px 0px;"/>
          </form>
        </div>
        <div class="col-md-12" v-if="post">
          <h4 style="margin: 30px 0px;">댓글 목록</h4>
          <div style="padding: 0px 10px;" v-for="comment in post.comment_set">
            <label>{{ comment.user.username }} - {{ comment.content }}</label>
            <input v-if="comment.user.username === userStore.user.username" class="btn btn-outline-danger btn-sm" style="margin: 0px 10px;" type="submit" value="삭제" @click="deleteComment(comment.id)" />
            <hr>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import { usePostStore } from "@/stores/post";
import { useCounterStore } from '@/stores/counter'
import { useRoute, useRouter } from "vue-router";

const store = usePostStore()
const router = useRouter()
const route = useRoute()
const post = ref("")
const content = ref("")
const userStore = useCounterStore()
const token = useCounterStore().token
const username = ref('')
onMounted(() => {
  store.getCategory();
});

onMounted(() => {
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/posts/${route.params.post_id}`,
    headers: {
      Authorization: `Token ${token}`
    }
  })
    .then((res) => {
      const updatedAt = new Date(res.data.updated_at)

      const formattedUpdatedAt = updatedAt.getFullYear() + '-' +
      (updatedAt.getMonth() + 1).toString().padStart(2, '0') + '-' +
      updatedAt.getDate().toString().padStart(2, '0') + ' ' +
      updatedAt.getHours().toString().padStart(2, '0') + ':' +
      updatedAt.getMinutes().toString().padStart(2, '0') + ':' +
      updatedAt.getSeconds().toString().padStart(2, '0');

      res.data.updated_at = formattedUpdatedAt
      post.value = res.data
      username.value = res.data.user.username
    })
    .catch((err) => console.log(err));
});

const updatePost = function (post) {
  router.push({ name: "postupdate", params: { post_id: post.id } });
};

const deletePost = function (post) {
  axios({
    method: "delete",
    url: `${store.API_URL}/api/v1/posts/${post}/`,
    headers: {
      Authorization: `Token ${token}`
    }
  }).then((res) => {
    router.push({ name: "post" })
  })
}

console.log(post)
const createComment = function () {
  axios({
    method : 'post',
    url: `${store.API_URL}/api/v1/posts/${route.params.post_id}/comments/`,
    data : {
      content : content.value
    },
    headers: {
      Authorization: `Token ${token}`
    }
  })
    .then((res)=>{
      post.value.comment_set.push(res.data)
      content.value = ''
      // username.value = res.data.user.username
    })
    .catch((err)=>{
      console.log(err);
    })
}

const deleteComment = function (commentId) {
  axios({
    method: 'delete',
    url: `${store.API_URL}/api/v1/comments/${commentId}`,
    headers: {
      Authorization: `Token ${token}`
    }
  })
  .then(res => {
    const index = post.value.comment_set.findIndex((post) => post.id === commentId)
    post.value.comment_set.splice(index, 1)
  })
  .catch(err => console.log(err))
}
</script>

<style scoped>

</style>
