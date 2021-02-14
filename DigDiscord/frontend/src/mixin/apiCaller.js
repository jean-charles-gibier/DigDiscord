
import axios from 'axios'
export default {
  data: () => ({
    message: 'message'
  }),
  methods: {
    async get_stat (request, title, explain) {
      try {
        axios.defaults.headers.common['Authorization'] =
          'Token 82bc819879697f1ee2503d3384c56dfc862bae3a'
        return {...await axios.get(request),
          request,
          'title': title,
          'explain': explain}
      } catch (err) {
        console.error(err)
      }
    },
    get_promise (request) {
      // todo : concurrent XHR get
    }
  }
}
