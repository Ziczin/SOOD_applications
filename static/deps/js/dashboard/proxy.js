export default async function dashboardProxy(make, me) {
  const csrfObj = await make.Query('/api/csrf-token').get()
  const qBase = make.Query('/api').via({"X-CSRFToken": csrfObj.csrfToken}).view();
  const roles = await qBase.at('roles').get()
  const departments = await qBase.at('departments').get()
  const qChangeRole = qBase.at('users').at(me.id).at("change_role").view()
  const qChangeDepartment = qBase.at('users').at(me.id).at("change_department").view()

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
            role.name, role.id,
            ...make.if(role.id === me.role.id,
              make.with.attrs('selected')
            )
          )
        ),
        make.on.change((e) => {
          qChangeRole.with({role: e.target.value}).patch()
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
            dep.name, dep.id,
            ...make.if(dep.id == me.department.id,
              make.with.attrs('selected')
            )
          )
        ),
        make.on.change((e) => {
          qChangeDepartment.with({department: e.target.value}).patch()
          .then(() => {
            location.reload()
          });
        })
      )
    )
  ]
}