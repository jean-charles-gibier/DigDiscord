import Vue from 'vue'
import Router from 'vue-router'
import Controller from '@/components/Controller'
import ChartContainer from '@/components/ChartContainer'
import Profile from '@/components/Profile'
import SignIn from '@/components/SignIn'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Controller',
      component: Controller
    },
    {
      path: '/chart',
      name: 'ChartContainer',
      component: ChartContainer
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile
    },
    {
      path: '/signin',
      name: 'SignIn',
      component: SignIn
    }
  ]
})
