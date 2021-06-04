
<template>
  <div class="container-fluid  p-10 " id="global-wrap">
    <div class="container-fluid p-0 ">
      <b-navbar toggleable="lg" type="dark" variant="info" style ="font-size: 1.5em !important">
        <b-navbar-brand href="#"><img src="./assets/Dig-discord2.svg" alt="Home" /></b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item-dropdown :text="dataLabelName" right>
              <b-dropdown-item v-for="(type, idx) in dataTypes" :key="idx" @click="dataType = idx" v-bind:href="'#/chart/'">{{dataLabels[idx]}}</b-dropdown-item>
            </b-nav-item-dropdown>
            <b-nav-item-dropdown :text="chartLabelName" right>
              <b-dropdown-item v-for="(type, idx) in chartTypes" :key="idx" @click="chartType = idx" v-bind:href="'#/chart/'">{{chartLabels[idx]}}</b-dropdown-item>
            </b-nav-item-dropdown>
            <b-nav-item v-bind:href="'#/chart/'" @click="dataType = dataTypes.indexOf('battle')">Bataille de mots</b-nav-item>
            <b-nav-item v-b-toggle.collapsible>A propos</b-nav-item>
            <b-nav-item v-b-toggle.settings>
              <svg  width="1em" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="cog" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="svg-inline--fa fa-cog fa-w-16 fa-lg"><path fill="currentColor" d="M487.4 315.7l-42.6-24.6c4.3-23.2 4.3-47 0-70.2l42.6-24.6c4.9-2.8 7.1-8.6 5.5-14-11.1-35.6-30-67.8-54.7-94.6-3.8-4.1-10-5.1-14.8-2.3L380.8 110c-17.9-15.4-38.5-27.3-60.8-35.1V25.8c0-5.6-3.9-10.5-9.4-11.7-36.7-8.2-74.3-7.8-109.2 0-5.5 1.2-9.4 6.1-9.4 11.7V75c-22.2 7.9-42.8 19.8-60.8 35.1L88.7 85.5c-4.9-2.8-11-1.9-14.8 2.3-24.7 26.7-43.6 58.9-54.7 94.6-1.7 5.4.6 11.2 5.5 14L67.3 221c-4.3 23.2-4.3 47 0 70.2l-42.6 24.6c-4.9 2.8-7.1 8.6-5.5 14 11.1 35.6 30 67.8 54.7 94.6 3.8 4.1 10 5.1 14.8 2.3l42.6-24.6c17.9 15.4 38.5 27.3 60.8 35.1v49.2c0 5.6 3.9 10.5 9.4 11.7 36.7 8.2 74.3 7.8 109.2 0 5.5-1.2 9.4-6.1 9.4-11.7v-49.2c22.2-7.9 42.8-19.8 60.8-35.1l42.6 24.6c4.9 2.8 11 1.9 14.8-2.3 24.7-26.7 43.6-58.9 54.7-94.6 1.5-5.5-.7-11.3-5.6-14.1zM256 336c-44.1 0-80-35.9-80-80s35.9-80 80-80 80 35.9 80 80-35.9 80-80 80z" class=""></path></svg>
            </b-nav-item>
          </b-navbar-nav>
          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <b-nav-form>
              <b-form-input v-model="searchInput" size="sm" class="mr-sm-2" placeholder="recherche full text"></b-form-input>
              <b-button size="sm" class="my-2 my-sm-0" type="submit" @click=" updateSearch() " v-bind:href="'#/chart/'">Rechercher</b-button>
            </b-nav-form>

            <b-nav-item-dropdown right>
              <!-- Using 'button-content' slot -->
              <template #button-content>
                <em>Utilisateur</em>
              </template>
              <b-dropdown-item href="#/profile/">Profile</b-dropdown-item>
              <b-dropdown-item href="#/signin/">Sign in / Sign out</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
    <div class="container-fluid" id="global-container">
      <b-collapse id="settings"> <!-- retractable -->
        <div class="container-fluid p-0" id="head-container">
          <div class="row">
            <div class="col-sm-4 bg-light">
              <div class="row">
                <div class="col">
                  Comptabiliser un contributeur au delà de {{ $store.state.slide_value }}
                  message{{ $store.state.slide_value > 1 ? 's' : '' }}
                  posté{{ $store.state.slide_value > 1 ? 's' : '' }} :
                </div>
              </div>
              <div class="row">
                <div class="col">
                  <vue-slider ref="slider" v-model="$store.state.slide_value" v-bind="options_slide" @change="setNbMinUserMessages()"></vue-slider>
                </div>
              </div>
            </div>
            <div class="col-sm-4 bg-light">
              <div class="row">
                <div class="col">
                  Entre (date de debut):
                </div>
              </div>
              <div class="row">
                <div class="col">
                  <b-form-datepicker v-model="$store.state.date_deb" v-bind="options_ddeb" @input="setDateDeb()"></b-form-datepicker>
                </div>
              </div>
            </div>
            <div class="col-sm-4 bg-light">
              <div class="row">
                <div class="col">
                  Et (date de fin):
                </div>
              </div>
              <div class="row">
                <div class="col">
                  <b-form-datepicker v-model="$store.state.date_fin" v-bind="options_dfin" @input="setDateFin()"></b-form-datepicker>
                </div>
              </div>
            </div>
          </div>
        </div>
      </b-collapse> <!-- fin du retractable  -->
    </div>
    <div class="container-fluid" id="global-container">
      <b-collapse id="collapsible"> <!-- retractable -->
        <div class="container-fluid p-0" id="head-container">
          <div class="row">
            <div class="col-sm-2 bg-success">
              <img class="card-img-top" src="./assets/DD_Gold_digger.png">
            </div>
            <div class="col-sm-10 card-body bg-warning m-12" style="font-family: 'Roboto', Ital">
<em>
Hello.<br>
Bienvenue sur DigDiscord.<br>
DigDiscord est le projet qui termine mon parcours DA python sur OpenClassrooms.<br>
La page d'accueil servira de blog technique par la même occasion<br>
DD explore et analyse le contenu des forums d'un serveur Discord (<a href="https://discord.gg/JdjVJ2WV">Ici DA Python</a>)<br>
Il présente les résultats via une API Django/DRF utilisable sur un front end basé sur Vue JS / axios / bootstrap.<br>
Il collecte les commentaires / mots clés / URL / "snipets" / extraits / utilisateurs / dates / images de votre serveur discord pour les présenter sous forme d'agrégats analytiques ou ludiques.<br>
Cela permet par exemple de suivre l'activité des forums ou des utilisateurs d'un serveur en présentant des statistiques suscitant l'intérêt des contributeurs.<br>
Ce projet est un "POC", une démonstration, une V.0 qui demande à être améliorée (et elle le sera 🙂). Toute contribution est bienvenue.<br>
L'API est (pour l'instant sommairement) exposée ici : <a href="https://jean-charles-gibier.org/api/swagger/">API</a>.<br>
Les sources sont disponibles ici : <a href="https://github.com/jean-charles-gibier/DigDiscord">DigDiscord</a>.<br>
<br>
Credit illustration : <a href="https://twitter.com/Kazhig">Adèle</a><br>
<!--
Current Token : {{ $store.state.user_token }}<br>
Date debut : {{ $store.state.date_deb }}<br>
Date fin : {{ $store.state.date_fin }}<br>
Nb min msg : {{ $store.state.slide_value }}<br>
-->
</em>
            </div>
          </div>
        </div>
      </b-collapse> <!-- fin du retractable  -->
      <div class="row">
        <div class="col-sm-12"  id="app-2">
          <router-view v-bind="{chartType: chartTypeName, dataType: dataTypeName, searchSelected: searchSelected}" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VueSlider from 'vue-slider-component'
import apiCaller from './mixin/apiCaller.js'
import 'vue-slider-component/theme/default.css'
export default {
  data: () => ({
    slide_value: '1',
    options_slide: {
      eventType: 'auto',
      width: 'auto',
      height: 5,
      dotSize: 16,
      min: 0,
      max: 50,
      interval: 1,
      show: true,
      speed: 1,
      tooltipDir: 'bottom',
      lazy: true
    },

    options_ddeb: {
      min: this.minDate,
      max: this.maxDate
    },

    options_dfin: {
      min: this.minDate,
      max: this.maxDate
    },

    date_deb: this.cmp_date_deb,
    date_fin: this.cmp_date_fin,
    message: {},
    chartType: 0,
    dataType: 0,
    searchInput: '',
    searchSelected: '',
    chartTypes: ['pie', 'curve', 'bar', 'line', 'json'],
    dataTypes: ['denombrements', 'scores_u', 'scores_c', 'frequences_l', 'frequences_f', 'frequences_u', 'distributions', 'battle'],
    chartLabels: ['Secteurs', 'Courbes', 'Histogrammes', 'Lignes', 'Contenu json'],
    dataLabels: ['Chiffres', 'Scores utilisateurs', 'Scores forums', 'Fréquences liens URL', 'Fréquences forums', 'Fréquences utilisateurs', 'Répartitions', 'Bataille de mots']
  }),
  watch: {
    dataType: function (newVal, oldVal) {
      this.searchSelected = ''
    },
    chartType: function (newVal, oldVal) {
      this.searchSelected = ''
    },
    date_deb: function (newVal, oldVal) {
      console.log('Prop changed: ', newVal, ' | was: ', oldVal)
      this.$store.commit('SET_DATE_DEB', newVal)
    },
    date_fin: function (newVal, oldVal) {
      console.log('Prop changed: ', newVal, ' | was: ', oldVal)
      this.$store.commit('SET_DATE_FIN', newVal)
    },
    slide_value: function (newVal, oldVal) {
      console.log('Prop changed: ', newVal, ' | was: ', oldVal)
      this.$store.commit('SET_SLIDE_VALUE', newVal)
    }
  },
  mixins: [apiCaller],
  components: {
    VueSlider
  },
  methods: {
    async writeBoundaryDates () {
      // => set max and min message dates and nb msg by user
    },
    async loadBoundaryDates () {
      // => get max and min message dates and nb msg by user
      var serviceUrl = 'http://127.0.0.1:8000/api/boundarydates/'
      var jsonDates = await this.get_stat(serviceUrl)
      console.log('jsonDates =' + JSON.stringify(jsonDates['data']))
      var firstMessageDate = jsonDates['data']['first_message_date']
      this.$store.commit('SET_DATE_DEB', firstMessageDate)
      var lastMessageDate = jsonDates['data']['last_message_date']
      this.$store.commit('SET_DATE_FIN', lastMessageDate)
    },
    updateSearch () {
      console.log('updateSearch for :' + this.searchInput)

      if (this.searchInput !== '') {
        console.log('updateSearch not empty for :' + this.searchInput)
        this.searchSelected = this.searchInput
        this.searchInput = ''
      }
    },
    async setDateDeb () {
      let dateDebResponse
      let payload = {'date_debut': this.$store.state.date_deb}
      let serviceUrl = 'http://127.0.0.1:8000/api/profile/'
      dateDebResponse = await this.put_profile(serviceUrl, payload)
      console.log(dateDebResponse)
    },
    async setDateFin () {
      let dateFinResponse
      let payload = {'date_fin': this.$store.state.date_fin}
      let serviceUrl = 'http://127.0.0.1:8000/api/profile/'
      dateFinResponse = await this.put_profile(serviceUrl, payload)
      console.log(dateFinResponse)
    },
    async setNbMinUserMessages () {
      let nbMinUserMessages
      let payload = {'nb_min_user_messages': this.$store.state.slide_value}
      let serviceUrl = 'http://127.0.0.1:8000/api/profile/'
      nbMinUserMessages = await this.put_profile(serviceUrl, payload)
      console.log(nbMinUserMessages)
    },
    dragEnd () {
      console.log('===========================================')
    }
  },
  computed: {
    now () {
      return new Date()
    },
    today () {
      return new Date(this.now.getFullYear(),
        this.now.getMonth(),
        this.now.getDate())
    },
    // 48 months prior
    minDate () {
      const minDate = new Date(this.$store.state.date_deb)
      minDate.setMonth(minDate.getMonth())
      return minDate
    },
    maxDate () {
    // maxdate = now
      const maxDate = new Date(this.$store.state.date_fin)
      maxDate.setMonth(maxDate.getMonth())
      return maxDate
    },
    chartTypeName () {
      return this.chartTypes[this.chartType]
    },
    dataTypeName () {
      return this.dataTypes[this.dataType]
    },
    dataLabelName () {
      return this.dataLabels[this.dataType]
    },
    chartLabelName () {
      return this.chartLabels[this.chartType]
    },
    slide_value () {
      return this.$store.slide_value
    }
  },
  mounted () {
    this.loadBoundaryDates()
  },
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Roboto', 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
img {
  display: block;
  max-width: 100%;
  height: auto;
}
@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;1,300&display=swap');
</style>
