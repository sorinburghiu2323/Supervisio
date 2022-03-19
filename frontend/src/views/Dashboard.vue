<template>
    <div class="container">
        <div class="title">
            Recommended projects
        </div>
        <div class="projects">
            <Project v-for="(project, index) in recommendedProjects" :key="index" :project="project"/>
        </div>
        <div class="title">
            Recommended supervisors
        </div>
        <div class="projects">
            <Supervisor v-for="(supervisor, index) in recommendedSupervisors" :key="index" :supervisor="supervisor"/>
        </div>
        <div class="title">
            Search everything
        </div>
        <div class="projects">
            <Project v-for="(project, index) in projects" :key="index" :project="project"/>
        </div>
    </div>
</template>
<script>
import axios from "axios";
import Project from "@/components/Project";
import Supervisor from "@/components/Supervisor";

export default {
    name: "Dashboard",
    components: {
        Project,
        Supervisor,
    },
    data() {
        return {
            projects: [],
            recommendedProjects: [],
            recommendedSupervisors: [],
        }
    },
    mounted() {
        this.getRecommendations();
        this.getProjects();
    },
    methods: {
        async getProjects() {
            await axios.get("api/projects/", { headers: { Authorization: this.$authToken } })
            .then((response) => {
                this.projects = response.data;
            })
            .catch((error) => {
                console.error(error);
            });
        },
        async getRecommendations() {
            await axios.get("api/projects/recommendations/", { headers: { Authorization: this.$authToken } })
            .then((response) => {
                this.recommendedProjects = response.data.projects;
                this.recommendedSupervisors = response.data.supervisors;
            })
            .catch((error) => {
                console.error(error);
            });
        },
    }
};
</script>
<style scoped>
.container {
    display: flex;
    flex-direction: column;
}
.title {
    margin-bottom: 20px;
    font-size: 50px;
    font-weight: bold;
    text-align: left;
    margin-left: 20px;
}
.projects {
    display: flex;
    flex-wrap: wrap;
    align-content: space-between;
}
</style>
