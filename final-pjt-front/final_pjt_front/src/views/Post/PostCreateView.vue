<template>
  <div class="wrapper">
    <div class="container content">
      <div class="margin-bottom-20 no-print" style="margin: 20px;"></div>
      <div class="row">
        <h1>게시글 생성</h1>
        <div class="margin-bottom-30"></div>
        <div class="col-md-12">
          <form class="form-horizontal" id="board_write_form" novalidate="novalidate" @submit.prevent="createPost">
            <div class="form-group">
              <label class="col-md-2 control-label" for="board_category">카테고리</label>
              <div class="col-md-2">
                <select class="form-control valid" aria-invalid="false" v-model="select">
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
                <button type="submit" class="btn btn-primary">글쓰기</button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
  <!-- <div>
    <h1>게시글 생성</h1>
    <form @submit.prevent="createPost">
      <label for="category">카테고리 선택:</label>
      <select v-model="select">
        <option v-for="category in store.category" :value="category.id">{{ category.name }}</option>
      </select>
      <label for="title">제목 : </label>
      <input type="text" id="title" v-model.trim="title">
      <label for="content">내용 : </label>
      <textarea name="content" id="content" cols="30" rows="10" v-model.trim="content"></textarea>
      <input type="submit" value="게시글 생성">
    </form>
  </div> -->
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import { usePostStore } from '@/stores/post'
  import axios from 'axios'
  import { useCounterStore } from '@/stores/counter';

  const select = ref('')
  const title = ref('')
  const content = ref('')

  const userStore = useCounterStore()
  const store = usePostStore()

  onMounted(() => {
    store.getCategory()
  })

  const createPost = function () {
    const post = {
      category: select.value,
      title: title.value,
      content: content.value,
    }
    console.log('createuser:', userStore.user)
    store.createPost(post)
    select.value = ''
    title.value = ''
    content.value = ''
  }
</script>

<style scoped>
  /* form {
    display: flex;
    flex-direction: column;
    width: 80%;
    margin: 20px auto;
  } */
</style>