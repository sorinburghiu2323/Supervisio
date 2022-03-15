import App from "./App.vue";
import Vue from "vue";
import router from "./router/router.js";


Vue.config.devtools = true;
Vue.config.productionTip = false;
Vue.prototype.$authToken = localStorage.authToken ? JSON.parse(localStorage.authToken) : "none";

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
