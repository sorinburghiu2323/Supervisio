<template>
    <div class="container">
        <div class="x" v-on:click="closePopup()">
            X
        </div>
        <div class="title" v-if="responseOutput">
            {{ responseOutput }}
        </div>
        <div class="title" v-if="!responseOutput">
            Submit application
        </div>
        <div class="description" v-if="!responseOutput">
            Message
        </div>
        <textarea v-model="message" class="input" rows=15 v-if="!responseOutput">
        </textarea>
        <button class="submit" @click="sendApplication()" v-if="!responseOutput"> Submit </button>
    </div>
</template>
<script>
import axios from "axios";

export default {
    name: "SubmitApplication",
    props: {
        projectId: Number,
    },
    data() {
        return {
            message: "",
            responseOutput: "",
        }
    },
    methods: {
        sendApplication() {
            axios.post(`/api/projects/${this.projectId}/apply/`, { message: this.message }, { headers: { Authorization: this.$authToken }})
            .then(
                this.responseOutput = "Application sent successfully."
            )
            .catch((error) => {
                console.error(error);
                this.responseOutput = error.response.data.detail;
            })
        },
        closePopup() {
            this.responseOutput = "";
            this.$emit('closePopup');
        }
    }
}
</script>
<style scoped>
.container {
    width: 30vw;
    height: 40vh;
    background-color: white;
    color: #1D9A75;
    padding: 15px;
    display: flex;
    flex-direction: column;
    border-radius: 15px;
    border-color: #1D9A75;
    border-style: solid;
}
.title {
    margin-bottom: 20px;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
    width: 80%;
    margin: auto;
}
.description {
    text-align: left;
    font-size: 15px;
}
.input {
    border-style: solid;
    border-color: #707070;
    border-radius: 10px;
    margin-top: 2vh;
    color: #1D9A75;
    font-size: 15px;
    padding: 10px;
    width: 94%;
    resize: none;
    margin-bottom: 15px;
}
.submit {
    border-style: solid;
    border-color: #707070;
    border-radius: 10px;
    background-color: #1D9A75;
    color: white;
    text-align: center;
    font-size: 20px;
    padding: 1vh 3vw 1vh 3vw;
    font-weight: bold;
    cursor: pointer;
    align-self: center;
}
.submit:hover {
    background-color: #187e5f;
}
.x {
    position: absolute;
    right: 15px;
    top: 5px;
    font-size: 45px;
    color: #1D9A75;
    cursor: pointer;
}
.x:hover {
    color: #156d52;
}
</style>
