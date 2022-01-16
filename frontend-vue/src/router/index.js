import Vue from 'vue'
import Router from 'vue-router'

// Containers
const TheContainer = () => import('@/containers/TheContainer')

// Views
const Login = () => import('@/views/Login')
const Search = () => import('@/views/Search')

// Manage
const Patent = () => import('@/views/manager/patent')
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
      redirect: '/searchmain',
      name: '메인',
      component: TheContainer,
      children: [
        {
          path: 'search',
          name: '검색',
          component:Search,
          props: true,
        },
        {
          path: 'manager',
          name: '관리',
          component: {
            render (c) { return c('router-view') }
          },
          children: [
            {
              path: 'patent',
              name: '특허문서관리',
              component: Patent
            },
            {
              path: 'markettingdata',
              name: '마케팅자료관리',
              component: MarkettingData
            },
            {
              path: 'notification',
              name: '공지사항관리',
              component: Notification
            },
            {
              path: 'techtrans',
              name: '기술이전문의관리',
              component: TechTrans
            },
            {
              path: 'smallpatent',
              name: '소액기술관리',
              component: SmallPatent
            },
            {
              path: 'popupzone',
              name: '팝업존관리',
              component: PopupZone
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

