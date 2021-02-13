
<template>
  <div class="container-fluid  p-10 " id="global-wrap">
    <div class="container-fluid p-0 ">
      <b-navbar toggleable="lg" type="dark" variant="info">
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
            <b-nav-item href="#" disabled>Bonus</b-nav-item>
          </b-navbar-nav>
          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <b-nav-form>
              <b-form-input size="sm" class="mr-sm-2" placeholder="Full text search"></b-form-input>
              <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
            </b-nav-form>

            <b-nav-item-dropdown right>
              <!-- Using 'button-content' slot -->
              <template #button-content>
                <em>User</em>
              </template>
              <b-dropdown-item href="#">Profile</b-dropdown-item>
              <b-dropdown-item href="#">Sign Out</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
    <div class="container-fluid" id="global-container">
      <b-collapse id="collapsible"> <!-- retractable -->
        <div class="container-fluid p-0" id="head-container">
          <div class="row">
            <div class="col-sm-2 bg-success">
              <img class="card-img-top" src="./assets/DD_Gold_digger.png">
            </div>
            <div class="col-sm-10 bg-warning d-flex justify-content-md-center align-items-center" style ="font-family: 'Roboto', Ital">
    Hello.<br>
    Ce "projet d'adoption" envisage d'explorer et d'analyser le contenu des forums d'un serveur Discord (Ici DA Python)<br>
    Il collecte les commentaires / mots clés / URL / "snipets" / extraits<br>
    utilisateurs / dates / images de votre serveur pour alimenter une base de données "full text".<br>
    Il présente les résultats via une API Django/DRF utilisable sur un front end basé sur Vue JS / axios / bootstrap.<br>
    Les sources sont (bien sûr) disponible ici : DigDiscord.
            </div>
          </div>
        </div>
      </b-collapse> <!-- fin du retractable  -->
      <div class="row">
        <div class="col-sm-12"  id="app-2">
          <router-view v-bind="{chartType: chartTypeName, dataType: dataTypeName}" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    message: {},
    chartType: 0,
    dataType: 0,
    chartTypes: ['pie', 'curve', 'bar', 'line', 'json'],
    dataTypes: ['denombrements', 'scores_u', 'scores_c', 'frequences_l', 'frequences_f', 'distributions', 'battle'],
    chartLabels: ['Secteurs', 'Courbes', 'Histogrammes', 'Lignes', 'Contenu json'],
    dataLabels: ['Chiffres', 'Scores utilisateurs', 'Scores forums', 'Fréquences liens URL', 'Fréquences forums', 'Répartitions', 'Bataille de mots']
  }),
  components: {
  },
  methods: {
  },
  computed: {
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
    }
  },
  mounted () {
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
