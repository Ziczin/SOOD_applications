export default function dashboardProxy(make, roles, currentUser, qRoles) {
  return [
    make.it.flexColumn,
    make.it.gap10px,
    make.h1('Панель управление прокси-юзера'),
    make.Separator(12),
    make.Div(
      make.it.flexRow,
      make.it.gap10px,
      make.it.centered,
      make.it.textCentered,
      make.Label("Роль: ", make.with.attr({for: "proxy-role"})),
      make.Select(
        ...roles.map(role => 
          make.Option(
            role.label,
            role.value,
            ...role.value == currentUser.role
            ? [make.with.attrs('selected')]
            : []
          )
        ),
        make.on.change((e) => {
          qRoles.with({
            username: currentUser.username,
            role: e.target.value,
          }).post().then(()=>{});
        })
      )
    )
  ]
}