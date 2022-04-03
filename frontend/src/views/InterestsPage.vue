<template>
    <div class="container">
        <div class="title">
            Adjust your interests
        </div>
        <div class="description">
            You are able to change these at any time from your settings
        </div>
        <div class="interests">
            <Interest 
            v-for="(interest, index) in interests" 
            :key="index" 
            :interest="interest"
            @clickInterest="clickInterest(interest)"
            />
        </div>
        <button class="save" @click="save()"> Save </button>
    </div>
</template>
<script>
import axios from "axios";
import Interest from "@/components/Interest";

export default {
    name: "InterestsPage",
    components: {
        Interest,
    },
    data() {
        return {
            interests: [],
            favouriteInterests: [],
        }
    },
    mounted() {
        this.getInterests();
    },
    methods: {
        async getInterests() {
            await axios.get("api/interests/", { headers: { Authorization: this.$authToken } })
            .then((response) => {
                this.interests = response.data;

                // Add favourite interests.
                this.favouriteInterests = this.interests.filter(interest => interest.is_favourite === true);
                this.favouriteInterests = this.favouriteInterests.map(function (obj) {
                    return obj.id;
                });
            })
            .catch((error) => {
                console.error(error);
            });
        },
        async save() {
            await axios.patch("api/interests/", { interests: `[${this.favouriteInterests}]` }, { headers: { Authorization: this.$authToken } })
            .then(() => {
                this.$router.push({ path: `/` })
            })
            .catch((error) => {
                console.error(error);
            });
        },
        clickInterest(interest) {
            if (this.favouriteInterests.includes(interest.id)) {
                let index = this.favouriteInterests.indexOf(interest.id);
                this.favouriteInterests.splice(index, 1);
            } else {
                this.favouriteInterests.push(interest.id);
            }
        }
    }
}
</script>
<style scoped>
.title {
    font-size: 50px;
    font-weight: bold;
}
.description {
    font-size: 25px;
    margin-bottom: 20px;
}
.interests {
    display: flex;
    flex-wrap: wrap;
    align-content: space-between;
    width: 60vw;
    margin: auto;
}
.save {
    margin-top: 20px;
    border-style: solid;
    border-color: #707070;
    border-radius: 10px;
    background-color: white;
    color: #1D9A75;
    text-align: center;
    font-size: 20px;
    padding: 1vh 3vw 1vh 3vw;
    font-weight: bold;
    cursor: pointer;
    align-self: center;
}
.save:hover {
    background-color: #e7e7e7;
}
</style>
