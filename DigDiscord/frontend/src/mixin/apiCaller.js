import axios from 'axios'
export default {
  data: () => ({
    message: 'message',
    service_token: ''
  }),
  methods: {
    async get_stat (request, title, explain) {
      console.log('get_stat ==>', request)
      console.log(' Current Token : ', this.$store.state.user_token)
      try {
        axios.defaults.headers.common['Authorization'] =
          'Token ' + this.$store.state.user_token
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
      console.log('post_profile ==>', request)
      console.log(' Current Token : ', this.$store.state.user_token)
      try {
        axios.defaults.headers.common['Authorization'] =
          'Token ' + this.$store.state.user_token
        await axios.post(request, data
        ).then(response => {
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
    async put_profile (request, data) {
      let finalRet = ''
      console.log('put_profile ==>', request)
      console.log(' Current Token : ', this.$store.state.user_token)
      try {
        axios.defaults.headers.common['Authorization'] =
          'Token ' + this.$store.state.user_token
        await axios.put(request, data
        ).then(response => {
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
      console.log('post_get_token ==>', request)
      console.log(' Current Token : ', this.$store.state.user_token)
      try {
        // axios.defaults.headers.common['Authorization'] =
        //  'Token ' + this.$store.state.user_token
        await axios.post(request, data
        ).then(response => {
          finalRet = response.data['token']
          return (response.data['token'])
        }).catch((err) => {
          var errstr = JSON.stringify(err.response.data)
          console.log(errstr)
          finalRet = errstr
        })
      } catch (ex) {
        console.log('Exception ==>', ex.message)
      } finally { }
      return finalRet
    },

    get_promise (request) {
      // todo : concurrent XHR get
    }
  }
}
