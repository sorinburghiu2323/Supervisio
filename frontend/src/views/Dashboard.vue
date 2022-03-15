<template>
    <div class="container">
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

export default {
    name: "Dashboard",
    components: {
        Project,
    },
    data() {
        return {
            projects: [],
        }
    },
    mounted() {
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
        }
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
