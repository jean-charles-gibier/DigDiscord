<script>
import { Bar } from 'vue-chartjs'
import loadDataSet from '../mixin/loadDataSet.js'

export default {
  extends: Bar,
  props: {
    messages: { type: Array, required: true },
    dataType: { type: String },
    chartType: { type: String },
    numMessage: { type: Number }
  },
  mixins: [loadDataSet],
  methods: {
    random_rgba () {
      var o = Math.round
      var r = Math.random
      var q = Math.sqrt
      var s = 192
      return 'rgba(' + o(r() * s) + ', ' + o(r() * s) + ', ' + o(r() * s) + ', ' + q(r()).toFixed(1) + ')'
    }
  },
  mounted () {
    const [title, explain, labels, values] = this.load_dataset(this.messages,
      {
        'title': 'Titre Bar',
        'chartType': 'bar',
        'dataType': this.dataType,
        'numMessage': this.numMessage
      })

    this.renderChart(
      {
        labels,
        datasets: [
          {
            label: explain,
            backgroundColor: this.random_rgba(),
            data: values
          }
        ]
      },
      {
        title: {
          display: true,
          text: title
        },
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          yAxes: [{
            ticks: {
              suggestedMin: 0
            }
          }]
        }
      }
    )
  }
}
</script>
