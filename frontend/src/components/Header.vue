<template>
    <div class="container">
        <div class="title">
            Supervisio
        </div>
        <div class="cog-icon">
            <font-awesome-icon :icon="['fas', 'cog']"/>
        </div>
    </div>
</template>
<script>
export default {
    name: "Header",
}
</script>
<style scoped>
.container {
    overflow: hidden;
    background-color: white;
    position: relative;
    padding: 10px;
    margin-bottom: 2vh;
}
.title {
    color: #1D9A75;
    font-size: 50px;
    font-weight: bold;
    text-align: center;
}
.cog-icon {
    position: absolute;
    right: 15px;
    top: 1.5vh;
    font-size: 45px;
    color: #1D9A75;
    cursor: pointer;
}
.cog-icon:hover {
    color: #125c46;
}
</style>
