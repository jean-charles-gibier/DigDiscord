import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // token generique
    user_token: '82bc819879697f1ee2503d3384c56dfc862bae3a',
    date_deb: '01-01-1900',
    date_fin: '01-01-1900',
    slide_value: 1
  },
  mutations: {
    SET_USER_TOKEN (state, payload) {
      state.user_token = String(payload)
    },
    SET_DATE_DEB (state, payload) {
      state.date_deb = String(payload)
    },
    SET_DATE_FIN (state, payload) {
      state.date_fin = String(payload)
    },
    SET_SLIDE_VALUE (state, payload) {
      state.slide_value = Number(payload)
    }
  },
  actions: {
  },
  modules: {
  }
})
