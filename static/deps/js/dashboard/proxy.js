export default function dashboardProxy(make, roles, departments, currentUser, qRoles, qDepartment) {
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
      make.it.leftAlign,
      make.Label("Роль: ",
        make.with.attr({for: "proxy-role"}),
        make.style.minWidth(60),
      ),
      make.Select(
        ...roles.map(role => 
          make.Option(
            role.label, role.value,
            ...role.value == currentUser.role
            ? [make.with.attrs('selected')] : []
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
      ),
    ),
    make.Div(
      make.it.flexRow,
      make.it.gap10px,
      make.it.centered,
      make.it.textCentered,
      make.it.leftAlign,
      make.Label("Отдел: ",
        make.with.attr({for: "proxy-department"}),
        make.style.minWidth(60),
      ),
      make.Select(
        ...departments.map(dep => 
          make.Option(
            dep.label, dep.value,
            ...dep.value == currentUser.department.name
            ? [make.with.attrs('selected')] : []
          )
        ),
        make.on.change((e) => {
          qDepartment.view()
          .at(currentUser.username)
          .with({
            department: e.target.value,
          })
          .patch()
          .then(()=>{
            //location.reload()
          });
        })
      )
    )
  ]
}