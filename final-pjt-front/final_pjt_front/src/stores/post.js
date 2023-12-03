import axios from 'axios'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'


export const usePostStore = defineStore('post', () => {
    const category = ref([])
    const posts = ref([])
    const commentCount = ref(0)
    const token = useCounterStore().token
    const router = useRouter()
    const API_URL = `http://127.0.0.1:8000`


    const getCategory = function () {
        axios({
            method: 'get',
            url: `${API_URL}/api/v1/category/`
        })
        .then(res => {
            console.log(res.data)
            category.value = res.data
        })
        .catch(err => console.log(err))
    }   

    const getPosts = function () {
        axios({
            method: 'get',
            url: `${API_URL}/api/v1/posts/`,
            headers: {
                Authorization: `Token ${token}`
            }
        })
        .then(res => {
            posts.value = res.data
            commentCount.value = res.data.comment_count
        })
        .catch(err => {
            console.log(err)
        })
    }

    const createPost = function ({category, title, content}) {
        axios({
            method: 'post',
            url: `${API_URL}/api/v1/posts/`,
            data: {
                category, title, content
            },
            headers: {
                Authorization: `Token ${token}`
            }
        })
        .then((res) => {
            console.log(res.data)
            router.push({ name: 'post' })
        })
        .catch(err => console.log(err))
    }
    return { posts, token, category, API_URL, getCategory, getPosts, createPost, commentCount }
})