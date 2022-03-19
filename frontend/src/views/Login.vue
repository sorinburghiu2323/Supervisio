<template>
    <div class="container">
        <div>
            <div class="title"> Supervisio </div>
            <div class="description"> You should have been given an account by your university </div>
        </div>
        <div class="inputs">
            <input class="input" v-model="email" type="text" placeholder="Email">
            <input class="input" v-model="password" type="password" placeholder="Password">
        </div>
        <button class="login" @click="loginUser()"> Sign in </button>
        <div class="error" v-if="error"> Email/password combination failed. </div>
    </div>
</template>
<script>
import axios from "axios";

export default {
    name: "Login",
    data() {
        return {
            email: "",
            password: "",
            error: false,
        }
    },
    methods: {
        loginUser() {
            axios.post("/api/users/login/", {email: this.email, password: this.password})
            .then((response) => {
                localStorage.authToken = JSON.stringify(response.data.token);
                this.$router.push("/");
                location.reload();  // To refresh authToken after redirect
            })
            .catch((error) => {
                console.error(error);
                this.error = true;
            })
        }
    }
}
</script>
<style scoped>
.container {
    margin: auto;
    margin-top: 10vh;
    background-color: white;
    width: 30vw;
    height: 50vh;
    border-radius: 25px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-direction: column;
    padding: 30px;
}
.title {
    color: #1D9A75;
    font-size: 50px;
    font-weight: bold;
}
.description {
    color: #1D9A75;
    font-size: 25px;
}
.inputs {
    display: flex;
    flex-direction: column;
}
.input {
    border-style: solid;
    border-color: #707070;
    border-radius: 10px;
    margin-top: 2vh;
    color: #1D9A75;
    font-size: 15px;
    padding: 10px;
    width: 15vw;
}
.input::placeholder {
    color: #1D9A75;
    font-family: inherit;
}
.login {
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
}
.login:hover {
    background-color: #187e5f;
}
.error {
    color: red;
}
</style>
