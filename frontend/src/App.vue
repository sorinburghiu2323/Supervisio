<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
body {
  min-height: 100vh;
  height: 100%;
  overflow: visible;
  background: rgb(0,175,70);
  background: linear-gradient(90deg, rgba(0,175,70,1) 0%, rgba(41,215,93,1) 35%, rgba(0,145,70,1) 82%);
}
#app {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
}
</style>
