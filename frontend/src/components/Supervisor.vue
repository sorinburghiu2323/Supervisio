<template>
    <div class="container" @click="$emit('clickSupervisor')">
        <div class="title">
            {{ supervisor.first_name }} {{ supervisor.last_name }}
        </div>
        <div class="description">
            {{ trimDescription(supervisor.bio) }}
        </div>
    </div>
</template>
<script>
export default {
    name: "Supervisor",
    props: {
        supervisor: Object,
    },
    methods: {
        trimDescription(text, length=200) {
            if (text && text.length > length) {
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
    height: 15vh;
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
    font-size: 25px;
    font-weight: bold;
}
.description {
    text-align: left;
    font-size: 15px;
}
</style>
