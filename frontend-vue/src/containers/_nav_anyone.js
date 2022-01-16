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
        _name: 'CSidebarNavItem',
        name: '소액기술 검색',
        to: '/manager/smallpatent',
        icon: { name: 'cil-text-shapes', class: 'text-white' },
      },
    ]
  }
]