<template>
  <div id="app">
    <Header v-if="this.$route.name !== 'Login'"/>
    <router-view/>
  </div>
</template>

<script>
import Header from "@/components/Header";

export default {
  name: 'App',
  components: {
    Header,
  }
}
</script>

<style>
body {
  margin: 0;
  min-height: 100vh;
  height: 100%;
  overflow: visible;
  background: rgb(0,175,70);
  background: linear-gradient(90deg, rgba(0,175,70,1) 0%, rgba(41,215,93,1) 35%, rgba(0,145,70,1) 82%);
}
#app {
  font-family: 'Montserrat', sans-serif;
  font-weight: 1000;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
}
</style>
