<template>
  <div class="wrapper" v-if="post">
    <div class="container content">
      <div class="margin-bottom-20 no-print" style="margin: 20px;"></div>
      <div class="row">
        <h1>게시글 수정 페이지</h1>
        <div class="margin-bottom-30"></div>
        <div class="col-md-12">
          <form class="form-horizontal" id="board_write_form" novalidate="novalidate" @submit.prevent="updatePost">
            <div class="form-group">
              <label class="col-md-2 control-label" for="board_category">카테고리</label>
              <div class="col-md-2">
                <select class="form-control valid" aria-invalid="false" v-model="selected">
                  <option v-for="category in store.category" :value="category.id">{{ category.name }}</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label class="col-md-2 control-label" for="board_subject">제목</label>
              <div class="col-md-5">
                <input type="text" class="form-control" placeholder name="board_subject" value v-model.trim="title">
              </div>
            </div>
            <div class="form-group">
              <label class="col-md-2 control-label" for="board_content">내용</label>
              <div class="col-md-10">
                <div class="redactor-styles redactor-in redactor-in-0 redactor-placeholder" style="min-height: 300px;">
                  <textarea name="board_content" id="board_content" rows="15" class="form-control change-to-redactor redactor-source" data-redactor-uuid="0" v-model="content"></textarea>
                </div>
              </div>
            </div>
            <div class="form-group">
              <div class="col-md-offset-2 col-md-10" style="margin-top: 15px;">
                <button type="submit" class="btn btn-primary">수정하기</button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { onMounted, ref } from 'vue'
  import { usePostStore } from '@/stores/post'
  import { useCounterStore } from '@/stores/counter'
  import { useRoute, useRouter } from 'vue-router'
  import axios from 'axios'


  const store = usePostStore()
  const route = useRoute()
  const router = useRouter()

  const post = ref('')
  const selected = ref('')
  const title = ref('')
  const content = ref('')
  const token = useCounterStore().token

  onMounted(() => {
    store.getCategory()
  })

  onMounted(() => {
    axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/posts/${route.params.post_id}`,
      headers: {
        Authorization: `Token ${token}`
      }
    })
    .then((res) => {
      console.log(res.data)
      post.value = res.data

      selected.value = res.data.category.id
      title.value = res.data.title
      content.value = res.data.content
    })
  })
  
  const updatePost = function () {
    console.log(selected.value, title.value, content.value)
    axios({
      method: 'put',
      url: `${store.API_URL}/api/v1/posts/${route.params.post_id}/`,
      data: {
        category: selected.value,
        title: title.value,
        content: content.value
      },
      headers: {
        Authorization: `Token ${token}`
      },
    })
    .then((res) => {
      router.push({ name: 'post' })
    })
  }
</script>

<style scoped>
 .update-form{
  display: flex;
  flex-direction: column;
  border: 1px solid black;
  margin: 25px;
  
 }
 .form-element{
  margin: 5px 15px;
 }
</style>