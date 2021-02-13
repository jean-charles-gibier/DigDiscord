import Vue from 'vue'
import Router from 'vue-router'
import Controller from '@/components/Controller'
import ChartContainer from '@/components/ChartContainer'

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
    }
  ]
})
