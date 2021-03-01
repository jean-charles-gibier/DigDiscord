
export default {
  data: () => ({
    labels: [],
    dataSet: [],
    title: 'default title'
  }),
  methods: {
    // data control
    load_dataset (messages, options) {
      if (messages === undefined ||
        messages[0] === undefined ||
        messages[0].data === undefined ||
        messages[0]['request'] === undefined) {
        console.log('Data or type undefined => return "No values" :\n')
        console.log('[' + JSON.stringify(this.messages) + ']')
        return ['No values', [], []]
      }

      const monthLabels = {
        '1': 'Janvier',
        '2': 'Février',
        '3': 'Mars',
        '4': 'Avril',
        '5': 'Mai',
        '6': 'Juin',
        '7': 'Juillet',
        '8': 'Août',
        '9': 'Septembre',
        '10': 'Octobre',
        '11': 'Novembre',
        '12': 'Décembre'
      }

      const weekDayLabels = {
        '1': 'Lundi',
        '2': 'Mardi',
        '3': 'Mercredi',
        '4': 'Jeudi',
        '5': 'Vendredi',
        '6': 'Samedi',
        '7': 'Dimanche'
      }

      // options settings
      // var chartType = options['chartType']
      var dataType = options['dataType']
      var numMessage = options['numMessage']
      var title = options['title']
      var explain = options['explain']
      var request = messages[numMessage]['request']
      var labelsLabel = 'aggregate_name'
      var dataSetLabel = 'count'

      // first: validate api json content
      var values = [
        'denombrements',
        'scores_c',
        'scores_u',
        'distributions',
        'battle'].includes(dataType) && !request.endsWith('api/distribution/') ? messages[numMessage].data : messages[numMessage].data.results

      // then validate the kind of content
      console.log('values', values)
      if (values === undefined) {
        console.log('result undefined !')
        return ['No values', [], []]
      }

      // On limite d'office les résultats aux 25 meilleurs scores
      values = values.slice(0, 25)

      // on traite chaque cas spécial de chaque stats
      if (dataType === 'frequences_l' || dataType === 'frequences_f' || dataType === 'frequences_u') {
        // for the moment we take only 30 firsts values
        if (request.endsWith('api/links/')) {
          labelsLabel = 'link_content'
          dataSetLabel = 'count_links'
        } else if (request.endsWith('api/channels/')) {
          labelsLabel = 'channel_name'
          dataSetLabel = 'count_messages'
        } else if (request.endsWith('api/score/')) {
          labelsLabel = 'user_name'
          dataSetLabel = 'count_messages'
        }
      }

      if (dataType === 'scores_c' || dataType === 'scores_u') {
        if (request.endsWith('by_user/')) {
          labelsLabel = 'channel_name'
          dataSetLabel = 'count_messages'
        }
        if (request.endsWith('by_channel/')) {
          labelsLabel = 'user_name'
          dataSetLabel = 'count_messages'
        }
      }

      if (dataType === 'battle') {
        let elem1 = {}
        let elem2 = {}
        elem1[labelsLabel] = values[0]['word_1']
        elem1[dataSetLabel] = values[0]['result_1']
        elem2[labelsLabel] = values[0]['word_2']
        elem2[dataSetLabel] = values[0]['result_2']
        values = [elem1, elem2]
      }

      // console.log('==>', values)
      values.forEach(element => {
        this.labels.push((request.endsWith('by_hour/') || request.endsWith('distribution/')) ? element[labelsLabel] + ' h' : request.endsWith('by_weekday/') ? weekDayLabels[element[labelsLabel]] : request.endsWith('by_month/') ? monthLabels[element[labelsLabel]] : element[labelsLabel])
        // console.log('word label', element[labelsLabel])
        this.dataSet.push(element[dataSetLabel])
        // console.log('word data', element[dataSetLabel])
      })

      // console.log('===>', messages[numMessage]['exp'])
      title = messages[numMessage]['title']
      explain = messages[numMessage]['explain']
      return [
        title,
        explain,
        this.labels,
        this.dataSet
      ]
    }
  }
}
