<template>
    <div class="container">
        <div class="stats">
            <div class="stat">
                <font-awesome-icon icon="fa-solid fa-eye" /> {{ project.views }}
            </div>
            <div class="stat">
                <font-awesome-icon icon="fa-solid fa-pen-to-square" /> {{ project.applications_count }}
            </div>
        </div>
        <div class="title">
            {{ project.title }}
        </div>
        <div class="title">
            {{ project.supervisor.first_name }} {{ project.supervisor.last_name }}
        </div>
        <div class="description">
            {{ project.description }}
        </div>
        <div class="title">
            About the supervisor
        </div>
        <div class="description">
            {{ project.supervisor.bio }}
        </div>
        <button class="apply" @click="showSubmitApplicationPopup()"> Apply </button>
        <div class="submit-application" v-if="showSubmitApplication">
            <SubmitApplication :projectId="project.id" @closePopup="closePopup()" />
        </div>
    </div>
</template>
<script>
import axios from "axios";
import SubmitApplication from "@/components/SubmitApplication";

export default {
    name: "ProjectPage",
    components: {
        SubmitApplication,
    },
    data() {
        return {
            project: Object,
            showSubmitApplication: false,
        }
    },
    mounted() {
        this.getProject();
    },
    methods: {
        async getProject() {
            await axios.get(`api/projects/${this.$route.params.id}/`, { headers: { Authorization: this.$authToken } })
            .then((response) => {
                this.project = response.data;
            })
            .catch((error) => {
                console.error(error);
            });
        },
        showSubmitApplicationPopup() {
            this.showSubmitApplication = true;
        },
        closePopup() {
            this.showSubmitApplication = false;
        }
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
