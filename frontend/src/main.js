import App from "./App.vue";
import Vue from "vue";
import router from "./router/router.js";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faCog, faEye, faPenToSquare } from "@fortawesome/free-solid-svg-icons";

Vue.component("font-awesome-icon", FontAwesomeIcon);
library.add(faCog, faEye, faPenToSquare);

Vue.config.devtools = true;
Vue.config.productionTip = false;
Vue.prototype.$authToken = localStorage.authToken ? JSON.parse(localStorage.authToken) : "none";

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
