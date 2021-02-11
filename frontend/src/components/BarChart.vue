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
  mounted () {
    const [title, labels, values] = this.load_dataset(this.messages,
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
            label: title,
            backgroundColor: '#f87979',
            data: values
          }
        ]
      },
      { responsive: true,
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
