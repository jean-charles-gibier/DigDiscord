<script>
import { Line } from 'vue-chartjs'
import loadDataSet from '../mixin/loadDataSet.js'

export default {
  extends: Line,
  props: {
    messages: { type: Array, required: true },
    dataType: { type: String },
    chartType: { type: String },
    numMessage: { type: Number }
  },
  mixins: [loadDataSet],
  mounted () {
    const [title, explain, labels, values] = this.load_dataset(this.messages,
      {
        'title': 'Titre Line',
        'chartType': 'line',
        'dataType': this.dataType,
        'numMessage': this.numMessage
      })

    this.renderChart(
      {
        labels,
        datasets: [
          {
            label: explain,
            backgroundColor: 'transparent',
            borderColor: 'rgba(1, 116, 188, 0.50)',
            pointBackgroundColor: 'rgba(171, 71, 188, 1)',
            data: values
          }
        ]
      },
      {
        responsive: true,
        maintainAspectRatio: false,
        title: {
          display: true,
          text: title
        },
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
