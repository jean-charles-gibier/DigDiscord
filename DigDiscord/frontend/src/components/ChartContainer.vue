<template>
  <div id='app'>
<!--
    <div>Item: {{ chartType }} / {{ dataType }}</div>
-->
      <div v-if="dataType === 'denombrements'">
        <div class="d-flex flex-row justify-content-around">
          <div class="card bg-light h2">
            <div class="card-body text-center">
            <p class="card-text">Chiffres du serveur {{cServerName}} au {{new Date().toJSON().slice(0,10).split('-').reverse().join('/') }}</p>
          </div>
        </div>
      </div>
        <div class="d-flex flex-row justify-content-around">
          <div class="card bg-light mb-3" style="max-width: 18rem;">
            <div class="card-header">
              <h5 class="card-title">Nombre d'utilisateurs</h5>
            </div>
            <div class="card-body">
              <div class="container-fluid">
                <div class="row">
                  <div class="col">
                      <p class="card-text h1">
                        {{cUserCount}}
                      </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="card bg-light mb-3" style="max-width: 18rem;">
            <div class="card-header">
              <h5 class="card-title">Nombre de forums</h5>
            </div>
            <div class="card-body">
              <div class="container-fluid">
                <div class="row">
                  <div class="col">
                      <p class="card-text h1">
                        {{cChannelCount}}
                      </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="card bg-light mb-3" style="max-width: 18rem;">
            <div class="card-header">
              <h5 class="card-title">Nombre de messages</h5>
            </div>
            <div class="card-body">
              <div class="container-fluid">
                <div class="row">
                  <div class="col">
                      <p class="card-text h1">
                        {{cMessageCount}}
                      </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="card bg-light mb-3" style="max-width: 18rem;">
            <div class="card-header">
              <h5 class="card-title">Nombre de liens</h5>
            </div>
            <div class="card-body">
              <div class="container-fluid">
                <div class="row">
                  <div class="col">
                      <p class="card-text h1">
                        {{cLinkCount}}
                      </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else>
        <div v-if="dataType === 'scores_u'" class="p-0">
          <!-- Explanations here -->
          <div class="card bg-light d-flex flex-row col-sm-12">
            <div class="col-sm-6">
              <div class="d-flex flex-row justify-content-center">
                <div class="h5 pt-1 pl-2 pr-2">
                  Utilisateur :
                </div>
                <div class="pt-1">
                  <select v-model="userSelected">
                    <option v-for="result in this.userList[0].data.results" v-bind:value="result.identifier" :key="result.identifier">
                      {{  result.name }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="dataType === 'scores_c'" class="p-0">
          <!-- Explanations here -->
          <div class="card bg-light d-flex flex-row col-sm-12">
            <div class="col-sm-6">
              <div class="d-flex flex-row justify-content-center col-sm-12">
                <div class="h5 pt-1 pl-2 pr-2">
                  Forum :
                </div>
                <div class="pt-1">
                  <select v-model="channelSelected">
                    <option v-for="result in this.channelList[0].data.results" v-bind:value="result.identifier" :key="result.identifier">
                      {{  result.name }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="dataType === 'battle'" class="p-0">
          <div class="card bg-light">
              <div class="row align-items-center flex-row">
                <div class="justify-content-center d-flex col-sm-5">
                <div class="h5 pt-1 pl-2 pr-2">
                  Mot #1 :
                </div>
                <div class="pt-0">
                  <b-form-input v-model="word1Selected" placeholder="Entrer mot #1"></b-form-input>
                </div>
              </div>

              <div class="justify-content-center d-flex col-sm-2">
                <div class="h5 pt-1 pl-2 pr-2">
                  <b-button pill @click="refreshValues()">VS</b-button>
                </div>
              </div>

              <div class="justify-content-center d-flex col-sm-5">
                <div class="h5 pt-1 pl-2 pr-2">
                  Mot #2 :
                </div>
                <div class="pt-0">
                  <b-form-input v-model="word2Selected" placeholder="Entrer mot #2"></b-form-input>
                </div>
              </div>
            </div>
          </div>
        </div>
<!-- EN CHANTIER -->
        <div v-if="dataType === 'distributions'" class="p-0">
          <div class="card bg-light">
              <div class="row align-items-center flex-row">
                <div class="justify-content-center d-flex col-sm-6 h5  pt-1 pl-2 pr-2">
                  <b-form-group label="Sélection" v-slot="{ ariaDescribedby }">
                      <b-form-radio-group
                        v-model="repartSelected"
                        :options="options"
                        :aria-describedby="ariaDescribedby"
                        name="plain-inline"
                        plain
                      ></b-form-radio-group>
                    </b-form-group>
                  </div>
                  <div class="justify-content-center d-flex col-sm-6" v-if="repartSelected !== 'generale'">

                    <div class="h5 pt-1 pl-2 pr-2" >
                      {{ repartSelected === 'generale' ? '' : repartSelected[0].toUpperCase() + repartSelected.substring(1) + ' :' }}
                    </div>
                    <div class="pt-1">
                      <div v-if="repartSelected === 'forum'">
                        <select v-model="uofSelected">
                          <option v-for="result in this.channelList[0].data.results" v-bind:value="result.identifier" :key="result.identifier">
                            {{  result.name }}
                          </option>
                        </select>
                      </div>
                      <div v-else>
                        <select v-model="uofSelected">
                          <option v-for="result in this.userList[0].data.results" v-bind:value="result.identifier" :key="result.identifier">
                            {{  result.name }}
                          </option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
<!-- FIN CHANTIER -->

        <div v-if="chartType === 'bar'">
          <div v-for="(message, idx) in messages" :key="idx">
            <BarChart
            :messages="messages"
            :dataType="dataType"
            :numMessage="idx"
            :key="idx" />
          </div>
        </div>

        <div v-if="chartType === 'curve'">
          <div v-for="(message, idx) in messages" :key="idx">
            <AreaChart
            :messages="messages"
            :dataType="dataType"
            :numMessage="idx"
            :key="idx" />
          </div>
        </div>

        <div v-if="chartType === 'pie'">
          <div v-for="(message, idx) in messages" :key="idx">
            <PieChart
            :messages="messages"
            :dataType="dataType"
            :numMessage="idx"
            :key="idx" />
          </div>
        </div>

        <div v-if="chartType === 'line'">
          <div v-for="(message, idx) in messages" :key="idx">
            <LineChart
            :messages="messages"
            :dataType="dataType"
            :numMessage="idx"
            :key="idx" />
            </div>
        </div>

        <div v-if="chartType === 'json'">
        </div>
      </div>
    </div>

</template>

<script>
import AreaChart from './AreaChart.vue'
import PieChart from './PieChart.vue'
import BarChart from './BarChart.vue'
import LineChart from './LineChart.vue'
import apiCaller from '../mixin/apiCaller.js'

export default {
  name: 'App',
  props: {
    dataType: { type: String },
    chartType: { type: String }
  },
  watch: {
    dataType: function (newVal, oldVal) {
      console.log('Prop changed: ', newVal, ' | was: ', oldVal)
      this.refreshValues()
    },
    userSelected: function (newVal, oldVal) {
      console.log('Prop changed: ', newVal, ' | was: ', oldVal)
      this.refreshValues()
    },
    channelSelected: function (newVal, oldVal) {
      console.log('Prop changed: ', newVal, ' | was: ', oldVal)
      this.refreshValues()
    },
    repartSelected: function (newVal, oldVal) {
      console.log('Prop changed: ', newVal, ' | was: ', oldVal)
      this.refreshValues()
    },
    uofSelected: function (newVal, oldVal) {
      console.log('Prop changed: ', newVal, ' | was: ', oldVal)
      this.refreshValues()
    }
  },
  mixins: [apiCaller],
  components: {
    AreaChart,
    PieChart,
    BarChart,
    LineChart
  },
  data: function () {
    return {
      messages: [],
      channelList: [],
      userList: [],
      userSelected: '0',
      channelSelected: '0',
      word1Selected: '',
      word2Selected: '',
      repartSelected: 'generale',
      uofSelected: '0',
      options: [
        { text: 'Générale', value: 'generale' },
        { text: 'Par utilisateur', value: 'utilisateur' },
        { text: 'Par forum', value: 'forum' }
      ]
    }
  },
  methods: {
    async loadUserList () {
      var serviceUrl = 'http://127.0.0.1:8000/api/user/'
      let nextUsers = await this.get_stat(serviceUrl)
      this.userList.push(nextUsers)
      // if there is more than one page ...
      while (nextUsers.data.next !== null) {
        // load next page
        nextUsers = await this.get_stat(nextUsers.data.next)
        // add users to main list
        this.userList[0].data.results.push(...nextUsers.data.results)
      }
      console.log('userList loaded')
    },
    async loadChannelList () {
      var serviceUrl = 'http://127.0.0.1:8000/api/channel/'
      this.channelList.push(await this.get_stat(serviceUrl))
      console.log('channelList loaded')
    },
    async refreshValues () {
      // prepare raw data to rendering
      // key is the dataType
      console.log('refreshValues')
      const translate = {
        'denombrements': ['channel/counter', 'link/counter', 'message/counter', 'user/counter', 'server/counter', 'server/'],
        'scores_u': 'score/<ID_USER>/by_user/',
        'scores_c': 'score/<ID_CHANNEL>/by_channel/',
        'distributions': ['distribution/',
          'distribution/<ID_CHANNEL>/by_channel/by_hour/',
          'distribution/<ID_CHANNEL>/by_channel/by_weekday/',
          'distribution/<ID_CHANNEL>/by_channel/by_month/',
          'distribution/<ID_USER>/by_user/by_hour/',
          'distribution/<ID_USER>/by_user/by_weekday/',
          'distribution/<ID_USER>/by_user/by_month/'
        ],
        'frequences_l': 'links/',
        'frequences_f': 'channels/',
        'battle': 'wordbattle/<WORD_1>/<WORD_2>/'
      }
      var endPoint = 'http://127.0.0.1:8000/api/'

      if (this.dataType !== undefined) {
        console.log('Type of data this.dataType :' + this.dataType)
        var translation = this.dataType
        // subPaths store endPoint of each request
        var subPaths = []
        var effectiveRequests = translate[translation]

        if (effectiveRequests !== undefined) {
          if (Object.prototype.toString.call(effectiveRequests) === '[object Array]') {
            for (var i = 0; i < effectiveRequests.length; i++) {
              subPaths[i] = effectiveRequests[i]
            }
          } else {
            subPaths[0] = effectiveRequests
          }
        }

        // clear messages contents
        console.log('clear messages contents')
        this.messages = []
        var nbPromises = subPaths.length
        // ask to our endpoint
        console.log('Loading promises ...')
        // let promisedRequests = []

        for (let o = 0; o < nbPromises; o++) {
          if (this.dataType === 'distributions') {
            console.log('in distributions :' + subPaths[o])
            if (subPaths[o].includes('<ID_USER>')) {
              console.log('includes <ID_USER> but :' + this.repartSelected)
              if (this.repartSelected === 'utilisateur') {
                console.log('repartSelected === utilisateur')
                subPaths[o] = subPaths[o].replace('<ID_USER>', this.uofSelected)
              } else {
                continue
              }
            }
            if (subPaths[o].includes('<ID_CHANNEL>')) {
              if (this.repartSelected === 'forum') {
                subPaths[o] = subPaths[o].replace('<ID_CHANNEL>', this.uofSelected)
              } else {
                continue
              }
            }
          }

          if (this.dataType === 'scores_u') {
            if (subPaths[o].includes('<ID_USER>')) {
              if (this.userSelected === undefined || this.userSelected === '0') {
                console.log('warn : <ID_USER> is undefined')
                continue
              }
              subPaths[o] = subPaths[o].replace('<ID_USER>', this.userSelected)
            }
          }
          if (this.dataType === 'scores_c') {
            if (subPaths[o].includes('<ID_CHANNEL>')) {
              if (this.channelSelected === undefined || this.channelSelected === '0') {
                console.log('warn : <ID_CHANNEL> is undefined')
                continue
              }
              subPaths[o] = subPaths[o].replace('<ID_CHANNEL>', this.channelSelected)
            }
          }
          if (this.dataType === 'battle') {
            if (subPaths[o].includes('<WORD_1>')) {
              if (this.word1Selected === undefined || this.word1Selected === '') {
                console.log('warn : <WORD_1> is undefined')
                continue
              }
              subPaths[o] = subPaths[o].replace('<WORD_1>', this.word1Selected)
            }
            if (subPaths[o].includes('<WORD_2>')) {
              if (this.word2Selected === undefined || this.word2Selected === '') {
                console.log('warn : <WORD_2> is undefined')
                continue
              }
              subPaths[o] = subPaths[o].replace('<WORD_2>', this.word2Selected)
            }
          }

          var serviceUrl = endPoint + subPaths[o]
          this.messages.push(await this.get_stat(serviceUrl))
        }
        console.log('=>' + JSON.stringify(this.messages))
      }
    }
    /*,
    upload () {
      const obj = {
        hello: 'world'
      }
      const json = JSON.stringify(obj)
      const blob = new Blob([json], {
        type: 'application/json'
      })
      const data = new FormData()
      data.append("document", blob);
      axios({
        method: 'post',
        url: '/sample',
        data: data,
      })
    }
    */
  },
  computed: {
    // dirty method caused by the following pb :
    // we launch 5 (or more) simultaneous requests
    cUserCount () {
      return this.messages[3] ? this.messages[3].data.UserCount.count : ''
    },
    cChannelCount () {
      return this.messages[0] ? this.messages[0].data.ChannelCount.count : ''
    },
    cLinkCount () {
      return this.messages[1] ? this.messages[1].data.LinkCount.count : ''
    },
    cServerCount () {
      return this.messages[4] ? this.messages[4].data.ServerCount.count : ''
    },
    cMessageCount () {
      return this.messages[2] ? this.messages[2].data.MessageCount.count : ''
    },
    cServerName () {
      return this.messages[5] ? this.messages[5].data.results[0].name : ''
    }
  },
  beforeMount: function () {
    console.log('beforeMount')
    this.refreshValues()
    this.loadUserList()
    this.loadChannelList()
  },
  mounted: function () {
    console.log('mounted')
    if (this.dataType !== undefined) {
      console.log('ChartContainer mounted this.messages :' + JSON.stringify(this.messages))
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
