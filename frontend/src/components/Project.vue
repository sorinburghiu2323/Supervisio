<template>
    <div class="container">
        <div class="title">
            {{ project.title }}
        </div>
        <div class="description">
            {{ trimDescription(project.description) }}
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
        }
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
