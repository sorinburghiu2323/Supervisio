<template>
    <div class="container">
        <div v-if="user.is_supervisor">
            <div class="title">
                Approved applications ({{ approvedApplications.length }})
            </div>
            <div class="projects">
                <Application v-for="(application, index) in approvedApplications" :key="index" :application="application"/>
            </div>
            <div class="title">
                Pending applications ({{ pendingApplications.length }})
            </div>
            <div class="projects">
                <Application v-for="(application, index) in pendingApplications" :key="index" :application="application"/>
            </div>
        </div>
        <div v-else>
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
                <Supervisor 
                    v-for="(supervisor, index) in recommendedSupervisors" 
                    :key="index" 
                    :supervisor="supervisor"
                    @clickSupervisor="clickSupervisorCard(supervisor)"    
                />
            </div>
            <div class="title">
                Search everything
            </div>
            <div class="filters">
                <font-awesome-icon class="search-icon" icon="fa-solid fa-magnifying-glass" @click="searchProjects()"/>
                <input class="input" v-model="search" type="text" placeholder="Search by phrase..">
                <div class="supervisor-filter">
                    <Multiselect 
                        v-model="searchSupervisor"
                        track-by="id"
                        label="last_name"
                        :custom-label="customLabel"
                        :options="supervisors"
                        :searchable="true"
                    />
                </div>
                <div class="interest-filter">
                    <Multiselect 
                        v-model="searchInterests"
                        track-by="id"
                        label="name"
                        :options="interests"
                        :searchable="false"
                        :multiple="true"
                        :close-on-select="false"
                    />
                </div>
            </div>
            <div class="projects">
                <Project v-for="(project, index) in projects" :key="index" :project="project"/>
            </div>
            <div v-if="projects === []" class="no-projects">
                Oops, we could not find any projects with this search..
            </div>
        </div>
    </div>
</template>
<script>
import axios from "axios";
import Project from "@/components/Project";
import Supervisor from "@/components/Supervisor";
import Application from "@/components/Application";
import Multiselect from 'vue-multiselect';

export default {
    name: "Dashboard",
    components: {
        Project,
        Supervisor,
        Application,
        Multiselect,
    },
    data() {
        return {
            user: null,
            projects: [],
            supervisors: [],
            interests: [],
            recommendedProjects: [],
            recommendedSupervisors: [],
            search: "",
            searchSupervisor: null,
            searchInterests: [],
            approvedApplications: [],
            pendingApplications: [],
        }
    },
    async mounted() {
        await this.getUser();
        if (this.user.is_supervisor) {
            this.getApprovedApplications();
            this.getPendingApplications();
        } else {
            this.getRecommendations();
            this.getProjects();
            this.getSupervisors();
            this.getInterests();
        }
    },
    methods: {
        async getUser() {
            await axios.get("api/users/me/", { headers: { Authorization: this.$authToken } })
            .then((response) => {
                this.user = response.data;
            })
            .catch((error) => {
                console.error(error);
            });
        },
        async getApprovedApplications() {
            await axios.get("api/projects/applications/?is_approved=true", { headers: { Authorization: this.$authToken } })
            .then((response) => {
                this.approvedApplications = response.data;
            })
            .catch((error) => {
                console.error(error);
            });
        },
        async getPendingApplications() {
            await axios.get("api/projects/applications/?is_approved=false", { headers: { Authorization: this.$authToken } })
            .then((response) => {
                this.pendingApplications = response.data;
            })
            .catch((error) => {
                console.error(error);
            });
        },
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
        async getSupervisors() {
            await axios.get("api/users/", { headers: { Authorization: this.$authToken } })
            .then((response) => {
                this.supervisors = response.data;
            })
            .catch((error) => {
                console.error(error);
            });
        },
        async getInterests() {
            await axios.get("api/interests/", { headers: { Authorization: this.$authToken } })
            .then((response) => {
                this.interests = response.data;
            })
            .catch((error) => {
                console.error(error);
            });
        },
        async searchProjects() {
            // Get data in right format.
            var interests = null;
            if (this.searchInterests.length != 0) {
                interests = `[${this.searchInterests.map(function (obj) { return obj.id;})}]`;
            }
            var supervisorId = null;
            if (this.searchSupervisor) {
                supervisorId = this.searchSupervisor.id;
            }

            // Make request.
            await axios.get(`api/projects/?phrase=${this.search}&supervisor=${supervisorId}&interests=${interests}`, 
                { headers: { Authorization: this.$authToken } })
            .then((response) => {
                this.projects = response.data;
            })
            .catch((error) => {
                console.error(error);
            });
        },
        clickSupervisorCard(supervisor) {
            this.search = "",
            this.searchSupervisor = supervisor,
            this.searchInterests = [],
            this.searchProjects();
        },
        customLabel({first_name, last_name}) {
            return `${first_name} ${last_name}`
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
.filters {
    display: flex;
    align-content: space-around;
    justify-content: left;
    margin-left: 20px;
}
.search-icon {
    font-size: 45px;
    cursor: pointer;
    margin-right: 20px;
}
.search-icon:hover {
    color: rgb(233, 233, 233);
}
.input {
    border-style: solid;
    border-color: #707070;
    border-radius: 10px;
    color: #1D9A75;
    font-size: 15px;
    padding: 10px;
    width: 15vw;
    margin-right: 2vw;
}
.input::placeholder {
    color: #1D9A75;
    font-family: inherit;
}
.supervisor-filter {
    border-style: solid;
    border-color: #707070;
    border-radius: 10px;
    margin-right: 2vw;
    width: 15vw;
}
.interest-filter {
    border-style: solid;
    border-color: #707070;
    border-radius: 10px;
    width: 22vw;
}
</style>
