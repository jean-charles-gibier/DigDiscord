<template>
  <div id=Profile class="text-center container h-100">
    <div class="alert alert-light">
      Veuillez compléter le formulaire<br>(vous obtiendrez un token pour interroger l'API)
    </div>
    <form id="contactForm" name="sentProfile" novalidate="novalidate" @submit="registerProfile">
      <div class="container">
        <div class="row align-items-stretch mb-5">
          <div class="col-md-6">
            <div class="form-group mb-md-0">
              <!-- first_name -->
              <input class="form-control" v-model="first_name" id="first_name" type="text" placeholder="Votre Prenom *" required="required" data-validation-required-message="Veuillez entrer votre prénom SVP.">
              <p class="help-block text-danger"></p>
            </div>
            <div class="form-group mb-md-0">
              <!-- last_name -->
              <input class="form-control" v-model="last_name" id="last_name" type="text" placeholder="Votre Nom *" required="required" data-validation-required-message="Veuillez entrer votre nom SVP.">
              <p class="help-block text-danger"></p>
            </div>
            <div class="form-group mb-md-0">
              <!-- email -->
              <input class="form-control" v-model="email" id="email" type="email" placeholder="Votre adresse mail *" required="required" data-validation-required-message="Veuillez entrer votre adresse mail SVP.">
              <p class="help-block text-danger"></p>
            </div>
          </div>
          <div class="col-md-6">
            <div class="form-group mb-md-0">
              <!-- discord_nickname -->
              <input class="form-control" v-model="pseudo" id="pseudo" type="text" placeholder="Votre pseudo DAP" data-validation-required-message="Veuillez entrer votre pseudo si vous en avez un.">
              <p class="help-block text-danger"></p>
            </div>
              <!-- password 1 -->
            <div class="form-group mb-md-0">
              <input class="form-control" v-model="password1" id="password1" type="password" placeholder="Votre Mot de Passe *" required="required" data-validation-required-message="Votre mot de passe SVP.">
              <p class="help-block text-danger"></p>
            </div>
              <!-- password 2 -->
            <div class="form-group mb-md-0">
              <input class="form-control" v-model="password2" id="password2" type="password" placeholder="Confirmez votre Mot de Passe *" required="required" data-validation-required-message="Votre mot de passe SVP.">
              <p class="help-block text-danger"></p>
            </div>
          </div>
        </div>
        <div class="row align-items-stretch mb-5">
          <div></div>
          <div class="col-md-12">
            <div class="text-center" v-if="profileResponse !== undefined">
              <div class= "card mb-15"  id="alert">
                {{ profileResponse }}
              </div>
            </div>
            <div class="text-center" v-if="profileResponse !== undefined || validToken !== undefined">
              <button class="btn btn-dark" @click="getToken()">Récupérez votre token</button>
              <input class="form-control text-center" v-model="validToken" />
            </div>

            <div class="text-center">
              <div id="success">
              </div>
              <b-button pill class="btn btn-primary btn-xl text-uppercase" id="sendProfileButton" type="submit">Enregistrer Votre Profil</b-button>
            </div>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>
<script>
import apiCaller from '../mixin/apiCaller.js'

export default {
  name: 'Profile',
  mixins: [apiCaller],
  data () {
    return {
      first_name: '',
      last_name: '',
      email: '',
      pseudo: '',
      password1: '',
      password2: '',
      profileResponse: undefined,
      validToken: undefined
    }
  },
  methods: {
    async registerProfile () {
      if (this.profileResponse === undefined) {
        this.profileResponse = ''
        let payload = {'discord_nickname': this.pseudo, 'location': 'Paris', 'record_date': (new Date()).toISOString().split('T')[0], 'uzer': {'username': this.pseudo, 'email': this.email, 'first_name': this.first_name, 'last_name': this.last_name, 'password': this.password1}}
        let serviceUrl1 = 'http://127.0.0.1:8000/api/profile/'
        this.profileResponse = await this.post_profile(serviceUrl1, payload)
        this.validToken = undefined
      }
    },
    async getToken () {
      // recherche le token
      let serviceUrl2 = 'http://127.0.0.1:8000/api/api-token-auth/'
      this.validToken = await this.post_get_token(serviceUrl2, 'username=' + this.email + '&password=' + this.password1)
      this.profileResponse = undefined
    }
  }
}
</script>
<style scoped>
</style>
