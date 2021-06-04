// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

// import VueGlobalVariable from 'vue'
import Vue from 'vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import App from './App'
import router from './router'

// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import store from './store'

// Make BootstrapVue available throughout project
Vue.use(BootstrapVue)
// install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.config.devtools = true
Vue.config.productionTip = false

/* eslint-disable no-new */
/* instance racine */
new Vue({
  el: '#app',
  router,
  components: { App },
  store,
  template: '<App/>'
})
