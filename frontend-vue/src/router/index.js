import Vue from 'vue'
import Router from 'vue-router'

// Containers
const TheContainer = () => import('@/containers/TheContainer')

// Views
const Login = () => import('@/views/Login')

// Manage
const InjectionData = () => import('@/views/manager/injectiondata')
const CncosciData = () => import('@/views/manager/cncoscidata')
const CncpowerData = () => import('@/views/manager/cncpowerdata')
const Users = () => import('@/views/manager/users')




Vue.use(Router)

export default new Router({
  mode: 'hash', // https://router.vuejs.org/api/#mode
  linkActiveClass: 'active',
  scrollBehavior: () => ({ y: 0 }),
  routes: configRoutes()
})

function configRoutes () {
  return [
    // {
    //   path: '/login',
    //   redirect: '/login',
    //   name: '로그인',
    //   component:Login,
    // },
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
              component: CncosciData
            },
            {
              path: 'cncpower',
              name: 'CNC 전력 데이터',
              component: CncpowerData
            },
            {
              path: 'users',
              name: '사용자관리',
              component: Users
            },
          ]
        },
     ]
    }
  ]
}

