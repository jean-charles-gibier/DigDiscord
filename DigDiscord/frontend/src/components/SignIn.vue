<template>
    <div id=Profile class="text-center container h-100">
        <div class="alert alert-light">
        </div>
        <form id="signInForm" name="signIn" novalidate="novalidate" @submit="getAll">
            <div class="container">
                <div class="row align-items-stretch mb-5">
                    <div class="col-md-6">
                        <div class="form-group mb-md-0">
                            <!-- email -->
                            <input class="form-control" v-model="email" id="email" type="email" placeholder="Votre adresse mail *" required="required" data-validation-required-message="Veuillez entrer votre adresse mail SVP.">
                            <p class="help-block text-danger"></p>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <!-- password 1 -->
                        <div class="form-group mb-md-0">
                            <input class="form-control" v-model="password1" id="password1" type="password" placeholder="Votre Mot de Passe *" required="required" data-validation-required-message="Votre mot de passe SVP.">
                            <p class="help-block text-danger"></p>
                        </div>
                    </div>
                </div>
                <div class="row align-items-stretch mb-5">
                    <div class="col-md-12">
                        <div class="text-center">
                            <div id="success">
                                <div class="text-center" v-if="validToken !== undefined">
                                    <div class= "card mb-15"  id="alert">
                                    {{ validToken }}
                                    </div>
                                </div>
                            </div>
                            <b-button pill class="btn btn-primary btn-xl text-uppercase" id="sendProfileButton" type="submit">Identifiez vous</b-button>
                        </div>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>
<script>
import apiCaller from '../mixin/apiCaller.js'
import { mapState } from 'vuex'

export default {
  name: 'Profile',
  mixins: [apiCaller],
  data () {
    return {
      email: '',
      password1: '',
      validToken: undefined
    }
  },
  methods: {
    async getAll () {
      await this.getToken()
      await this.getProfile()
    },
    async getToken () {
      // recherche le token
      let serviceUrl = 'http://127.0.0.1:8000/api/api-token-auth/'
      this.validToken = await this.post_get_token(serviceUrl, 'username=' + this.email + '&password=' + this.password1)
      console.log('on getToken Token: ', this.validToken)
      let hex = /^[a-fA-F0-9]+$/i
      let match = this.validToken.match(hex)
      if (match) {
        this.$store.commit('SET_USER_TOKEN', this.validToken)
      }
    },
    async getProfile () {
      // recherche les infos associées
      let serviceUrl = 'http://127.0.0.1:8000/api/profile/'
      this.profile = await this.get_stat(serviceUrl, '', '')
      console.log('on getProfile Token: ', this.profile)
      console.log('on getProfile Token: ', this.validToken, ' profile.date_debut: ', this.profile.data.date_debut, ' profile.date_fin: ', this.profile.data.date_fin)
      this.$store.commit('SET_DATE_DEB', this.profile.data.date_debut)
      this.$store.commit('SET_DATE_FIN', this.profile.data.date_fin)
      this.$store.commit('SET_SLIDE_VALUE', this.profile.data.nb_min_user_messages)
    }
  },
  computed: {
    ...mapState(['user_token'])
  }
}
</script>
<style scoped>
</style>
