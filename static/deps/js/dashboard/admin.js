export default function dashboardAdmin(make) {
  const btns = [
    {
      text: 'Управление формами',
      loc: '/applications/forms-manager/',
    },
    {
      text: 'Управление отделом',
      loc: '/applications/users-manager/',
    },
    {
      text: 'Управление перечислениями',
      loc: '/applications/enums-manager/',
    },
    {
      text: 'Управление услугами',
      loc: '/applications/services-manager/',
    },
  ]
  return [
    make.it.flexColumn,
    make.style.gap(6),
    ...btns.map(btn =>
      make.Div(
        make.it.marginOnHover,
        make.Button(
          make.it.redir,
          make.with.text(btn.text),
          make.on.click(() => {
            window.location.href = btn.loc
          })
        )
      )
      
    )
  ]
}