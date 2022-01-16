export default [
  {
    _name: 'CSidebarNav',
    _children: [
      {
        _name: 'CSidebarNavItem',
        name: '특허 검색',
        to: '/search',
        icon: 'cil-search',
      },
      {
        _name: 'CSidebarNavTitle',
        _children: ['관리']
      },
      {
        _name: 'CSidebarNavItem',
        name: '특허문서관리',
        to: '/manager/patent',
        icon: 'cil-layers',
      },
      // {
      //   _name: 'CSidebarNavItem',
      //   name: '마케팅자료관리',
      //   to: '/manager/markettingdata',
      //   icon: 'cil-basket',
      // },
      // {
      //   _name: 'CSidebarNavItem',
      //   name: '공지사항관리',
      //   to: '/manager/notification',
      //   icon: { name: 'cil-task', class: 'text-white' },
      // },
      {
        _name: 'CSidebarNavItem',
        name: '기술이전문의관리',
        to: '/manager/techtrans',
        icon: { name: 'cil-list-high-priority', class: 'text-white' },
      },
      {
        _name: 'CSidebarNavItem',
        name: '소액기술관리',
        to: '/manager/smallpatent',
        icon: { name: 'cil-badge', class: 'text-white' },
      },
      {
        _name: 'CSidebarNavItem',
        name: '팝업존관리',
        to: '/manager/popupzone',
        icon: { name: 'cil-text-shapes', class: 'text-white' },
      },
      {
        _name: 'CSidebarNavItem',
        name: '통계관리',
        to: '/manager/statisticslogs',
        icon: { name: 'cil-chart-pie', class: 'text-white' },
      },
    ]
  }
]