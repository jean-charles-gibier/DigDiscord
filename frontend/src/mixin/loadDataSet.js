
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

      // options settings
      // var chartType = options['chartType']
      var dataType = options['dataType']
      var numMessage = options['numMessage']
      var title = options['title']
      var request = messages[numMessage]['request']
      var labelsLabel = 'aggregate_name'
      var dataSetLabel = 'count'

      // first: validate content
      var values = [
        'denombrements',
        'scores_c',
        'scores_u',
        'distributions',
        'battle'].includes(dataType) && !request.endsWith('api/distribution/') ? messages[numMessage].data : messages[numMessage].data.results

      console.log('values', values)
      if (values === undefined) {
        console.log('result undefined => autre traitement à prévoir')
        return ['No values', [], []]
      }

      // C'est ci qu'on traite chaque cas spécial de chaque stats
      if (dataType === 'frequences_l' || dataType === 'frequences_f') {
        // for the moment we take only 30 firsts values
        values = values.slice(0, 20)
        if (request.endsWith('api/links/')) {
          labelsLabel = 'link_content'
          dataSetLabel = 'count_links'
        } else if (request.endsWith('api/channels/')) {
          labelsLabel = 'channel_name'
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

      console.log('==>', values)

      values.forEach(element => {
        this.labels.push(element[labelsLabel])
        console.log('word label', element[labelsLabel])
        this.dataSet.push(element[dataSetLabel])
        console.log('word data', element[dataSetLabel])
      })

      return [
        title,
        this.labels,
        this.dataSet
      ]
    }
  }
}
