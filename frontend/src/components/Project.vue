<template>
    <div class="container">
        <div class="title">
            {{ project.title }}
        </div>
        <div class="description">
            {{ project.description }}
        </div>
    </div>
</template>
<script>
export default {
    name: "Project",
    props: {
        project: Object,
    }
}
</script>
<style scoped>
.container {
    margin: 10px;
    width: 30vw;
    height: 30vh;
}
.title {
    margin-bottom: 10px;
}
</style>
