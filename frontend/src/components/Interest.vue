<template>
    <div :class="containerClass" @click="clickContainer()">
        {{ interest.name }}
    </div>
</template>
<script>
export default {
    name: "Application",
    props: {
        interest: Object,
    },
    data() {
        return {
            containerClass: "unselected-container",
        }
    },
    mounted() {
        if (this.interest.is_favourite) {
            this.containerClass = "selected-container";
        }
    },
    methods: {
        clickContainer() {
            this.$emit("clickInterest");
            if (this.containerClass == "selected-container") {
                this.containerClass = "unselected-container";
            } else {
                this.containerClass = "selected-container";
            }
        }
    }
}
</script>
<style scoped>
.selected-container {
    position: relative;
    margin: 20px;
    width: 15vw;
    height: 3vh;
    background-color: yellow;
    color: #1D9A75;
    padding: 15px;
    border-radius: 15px;
    cursor: pointer;
}
.selected-container:hover {
    background-color: rgb(255, 255, 140);
}
.unselected-container {
    position: relative;
    margin: 20px;
    width: 15vw;
    height: 3vh;
    background-color: white;
    color: #1D9A75;
    padding: 15px;
    border-radius: 15px;
    cursor: pointer;
}
.unselected-container:hover {
    background-color: rgb(235, 235, 235);
}
</style>
