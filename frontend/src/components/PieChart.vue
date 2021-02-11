<script>
import { Pie } from 'vue-chartjs'
import loadDataSet from '../mixin/loadDataSet.js'

export default {
  extends: Pie,
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
      var s = 255
      return 'rgba(' + o(r() * s) + ', ' + o(r() * s) + ', ' + o(r() * s) + ', ' + r().toFixed(1) + ')'
    }
  },
  mounted () {
    const [title, labels, values] = this.load_dataset(this.messages,
      {
        'title': 'Titre Pie',
        'chartType': 'pie',
        'dataType': this.dataType,
        'numMessage': this.numMessage
      })

    this.gradient = this.$refs.canvas
      .getContext('2d')
      .createLinearGradient(0, 0, 0, 450)
    this.gradient2 = this.$refs.canvas
      .getContext('2d')
      .createLinearGradient(0, 0, 0, 450)

    this.gradient.addColorStop(0, 'rgba(255, 0,0, 0.5)')
    this.gradient.addColorStop(0.5, 'rgba(255, 0, 0, 0.25)')
    this.gradient.addColorStop(1, 'rgba(255, 0, 0, 0)')

    this.gradient2.addColorStop(0, 'rgba(0, 231, 255, 0.9)')
    this.gradient2.addColorStop(0.5, 'rgba(0, 231, 255, 0.25)')
    this.gradient2.addColorStop(1, 'rgba(0, 231, 255, 0)')
    var nbValues = labels.length
    var allGradients = Array.apply(null, {length: nbValues})
    for (var i = 0; i < nbValues; ++i) {
      allGradients[i] = this.random_rgba()
    }
    this.renderChart(
      {
        labels,
        datasets: [
          {
            label: title,
            backgroundColor: allGradients,
            data: values
          }
        ]
      },
      { responsive: true, maintainAspectRatio: false }
    )
  }
}
</script>
