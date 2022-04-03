<template>
    <div class="container" @click="goToApplication()">
        <div class="title">
            {{ application.project.title }}
        </div>
        <div class="description">
            {{ trimDescription(application.message) }}
        </div>
        <div class="supervisor">
            {{ application.student.first_name }} {{ application.student.last_name }}
        </div>
    </div>
</template>
<script>
export default {
    name: "Application",
    props: {
        application: Object,
    },
    methods: {
        trimDescription(text, length=200) {
            if (text.length > length) {
                return text.substring(0, length) + " ..."
            }
            return text;
        },
        goToApplication() {
            if (this.application.status !== "approved") {
                this.$router.push({ path: `/applications/${this.application.id}` })
            }
        },
    }
}
</script>
<style scoped>
.container {
    position: relative;
    margin: 20px;
    width: 28vw;
    height: 22vh;
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
