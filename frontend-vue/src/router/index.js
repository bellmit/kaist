import Vue from 'vue'
import Router from 'vue-router'

// Containers
const TheContainer = () => import('@/containers/TheContainer')

// Views
const Login = () => import('@/views/Login')

// Manage
const InjectionData = () => import('@/views/manager/injectiondata')
const Notification = () => import('@/views/manager/notification')
const TechTrans = () => import('@/views/manager/TechTrans')
const MarkettingData = () => import('@/views/manager/markettingdata')
const SmallPatent = () => import('@/views/manager/SmallPatent')
const PopupZone = () => import('@/views/manager/PopupZone')
const StatisticsLogs = () => import('@/views/manager/StatisticsLogs')


// Views - Pages
const Page404 = () => import('@/views/pages/Page404')
const Page500 = () => import('@/views/pages/Page500')
const Register = () => import('@/views/pages/Register')



Vue.use(Router)

export default new Router({
  mode: 'hash', // https://router.vuejs.org/api/#mode
  linkActiveClass: 'active',
  scrollBehavior: () => ({ y: 0 }),
  routes: configRoutes()
})

function configRoutes () {
  return [
    {
      path: '/login',
      redirect: '/login',
      name: '로그인',
      component:Login,
    },
    {
      path: '/',
      redirect: '/login',
      name: '메인',
      component: TheContainer,
      children: [
        {
          path: 'manager',
          name: '관리',
          component: {
            render (c) { return c('router-view') }
          },
          children: [
            {
              path: 'injectiondata',
              name: '사출기 데이터',
              component: InjectionData
            },
            {
              path: 'cncoscidata',
              name: 'CNC 진동 데이터',
              component: InjectionData
            },
            {
              path: 'cncpower',
              name: 'CNC 전력 데이터',
              component: InjectionData
            },
            {
              path: 'statisticslogs',
              name: '통계관리',
              component: StatisticsLogs
            },
          ]
        },
     ]
    },
    {
      path: '/pages',
      redirect: '/pages/404',
      name: 'Pages',
      component: {
        render (c) { return c('router-view') }
      },
      children: [
        {
          path: '404',
          name: 'Page404',
          component: Page404
        },
        {
          path: '500',
          name: 'Page500',
          component: Page500
        },
        {
          path: 'register',
          name: 'Register',
          component: Register
        },
      ]
    },
  ]
}

