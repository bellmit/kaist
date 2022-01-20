export default [
  {
    _name: 'CSidebarNav',
    _children: [
      {
        _name: 'CSidebarNavItem',
        name: '사출기 데이터',
        to: '/manager/injectiondata',
        icon: 'cil-layers',
      },
      {
        _name: 'CSidebarNavItem',
        name: 'CNC 진동 데이터',
        to: '/manager/cncoscidata',
        icon: { name: 'cil-list-high-priority', class: 'text-white' },
      },
      {
        _name: 'CSidebarNavItem',
        name: 'CNC 전력 데이터',
        to: '/manager/cncpower',
        icon: { name: 'cil-badge', class: 'text-white' },
      },
      {
        _name: 'CSidebarNavItem',
        name: '주피터허브',
        href: 'http://172.30.77.193:39470',
        target:"_blank",
        icon: { name: 'cil-chart-pie', class: 'text-white' },
      },
    ]
  }
]