
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
    async post_profile (request, data) {
      let finalRet = ''
      try {
        axios.defaults.headers.common['Authorization'] =
          'Token 82bc819879697f1ee2503d3384c56dfc862bae3a'
        await axios.post(request, data, {
          headers: {
            'contentType': 'application/json'
          }
        }).then(response => {
          return (response)
        }).catch((err) => {
          var errstr = JSON.stringify(err.response.data)
          console.log(errstr)
          finalRet = errstr
        })
      } catch (ex) {
        console.log('==>', ex.message)
      } finally { }
      return finalRet
    },
    async post_get_token (request, data) {
      let finalRet = ''
      try {
        await axios.post(request, data, {
          headers: {
            'contentType': 'application/json'
          }
        }).then(response => {
          finalRet = response.data['token']
          return (response.data['token'])
        }).catch((err) => {
          var errstr = JSON.stringify(err.response.data)
          console.log(errstr)
          finalRet = errstr
        })
      } catch (ex) {
        console.log('==>', ex.message)
      } finally { }
      return finalRet
    },

    get_promise (request) {
      // todo : concurrent XHR get
    }
  }
}
