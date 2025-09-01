export default function dashboardProxy(make, roles, currentUser, qRoles) {
  return [
    make.it.flexColumn,
    make.it.gap10px,
    make.Div(
     make.h1('Панель управления'),
      make.h1('прокси-юзера'),
    ),
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
          qRoles.view()
          .at(currentUser.username)
          .with({
            role: e.target.value,
          })
          .patch()
          .then(()=>{
            location.reload()
          });
        })
      )
    )
  ]
}