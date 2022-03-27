<template>
    <div class="container" @click="goToProject()">
        <div class="title">
            {{ project.title }}
        </div>
        <div class="description">
            {{ trimDescription(project.description) }} 
            <br> <br>
            Area:
            <br>
            {{ getInterests() }}
        </div>
        <div class="supervisor">
            {{ project.supervisor.first_name }} {{ project.supervisor.last_name }}
        </div>
    </div>
</template>
<script>
export default {
    name: "Project",
    props: {
        project: Object,
    },
    methods: {
        trimDescription(text, length=200) {
            if (text.length > length) {
                return text.substring(0, length) + " ..."
            }
            return text;
        },
        goToProject() {
            this.$router.push({ path: `/projects/${this.project.id}` })
        },
        getInterests() {
            return this.project.interests.map(function (obj) { return obj.name; }).join(', ')
        },
    }
}
</script>
<style scoped>
.container {
    position: relative;
    margin: 20px;
    width: 28vw;
    height: 28vh;
    background-color: white;
    color: #1D9A75;
    padding: 15px;
    display: flex;
    flex-direction: column;
    border-radius: 15px;
    cursor: pointer;
}
.container:hover {
    background-color: rgb(235, 235, 235);
}
.title {
    margin-bottom: 20px;
    text-align: center;
    font-size: 25px;
    font-weight: bold;
}
.description {
    text-align: left;
    font-size: 15px;
}
.supervisor {
    position: absolute;
    bottom: 15px;
    left: 15px;
    font-size: 20px;
    font-weight: bold;
}
</style>
