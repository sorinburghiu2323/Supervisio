<template>
    <div class="container">
        <div class="title">
            {{ application.project.title }}
        </div>
        <div class="title">
            {{ application.student.first_name }} {{ application.student.last_name }}
        </div>
        <div class="description">
            {{ application.message }}
        </div>
        <button class="apply" @click="review(true)"> Approve </button> <br> <br>
        <button class="apply" @click="review(false)"> Decline </button>
    </div>
</template>
<script>
import axios from "axios";

export default {
    name: "ApplicationPage",
    data() {
        return {
            application: Object,
        }
    },
    mounted() {
        this.getApplication();
    },
    methods: {
        async getApplication() {
            await axios.get(`api/projects/applications/${this.$route.params.id}/`, { headers: { Authorization: this.$authToken } })
            .then((response) => {
                this.application = response.data;
            })
            .catch((error) => {
                console.error(error);
            });
        },
        async review(is_approved) {
            await axios.post(`api/projects/applications/${this.$route.params.id}/review/`, { is_approved: is_approved }, { headers: { Authorization: this.$authToken } })
            .then(() => {
                this.$router.push({ path: `/` })
            })
            .catch((error) => {
                console.error(error);
            });
        },
    }
}
</script>
<style scoped>
.container {
    display: flex;
    flex-direction: column;
    margin-left: 20px;
}
.title {
    margin-bottom: 20px;
    font-size: 50px;
    font-weight: bold;
    text-align: left;
    width: 80vw;
}
.description {
    text-align: left;
    font-size: 15px;
    margin-bottom: 20px;
}
.apply {
    border-style: solid;
    border-color: #707070;
    border-radius: 10px;
    background-color: white;
    color: #1D9A75;
    text-align: center;
    font-size: 20px;
    padding: 1vh 3vw 1vh 3vw;
    font-weight: bold;
    cursor: pointer;
    align-self: center;
}
.apply:hover {
    background-color: #e7e7e7;
}
.stats {
    position: absolute;
    display: flex;
    flex-direction: column;
    right: 15px;
}
.stat {
    top: 1.5vh;
    font-size: 45px;
    color: white;
}
.submit-application {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
</style>
