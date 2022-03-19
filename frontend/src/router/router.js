import Vue from "vue";
import VueRouter from "vue-router";
import Dashboard from "../views/Dashboard.vue";
import Login from "../views/Login.vue";
import ProjectPage from "../views/ProjectPage.vue";
import axios from "axios";


Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Dashboard",
    component: Dashboard,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/projects/:id",
    name: "ProjectPage",
    component: ProjectPage,
  }
];

const router = new VueRouter({
  routes,
});

// Catch common status codes.
axios.interceptors.response.use(function (response) {
  return response
}, function (error) {
  if (error.response.status === 401) {
    router.push('/login')
  }
  return Promise.reject(error)
})

export default router;
