export default (make) =>
async function dashboardProxy(me) {
  const makeIt = make.it
  const csrfObj = await make.Query('/api/csrf-token').get()
  const qBase = make.Query('/api').via({"X-CSRFToken": csrfObj.csrfToken}).view();
  const rolesProm = await qBase.at('roles').get()
  const departmentsProm = await qBase.at('departments').get()
  const qChangeRole = qBase.at('users').at(me.id).at("change_role").view()
  const qChangeDepartment = qBase.at('users').at(me.id).at("change_department").view()

  const btns = [
    {
      text: 'Управление отделами',
      loc: '/applications/departments-manager/',
    },
  ]

  const [roles, departments] = await Promise.all([rolesProm, departmentsProm])
  return [
    makeIt.flexColumn,
    makeIt.gap10px,
    make.Div(
      make.h1('Панель управления'),
      make.h1('прокси-юзера'),
    ),
    make.Div(
      makeIt.flexRow,
      makeIt.gap10px,
      makeIt.centered,
      makeIt.textCentered,
      makeIt.leftAlign,
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
      makeIt.flexRow,
      makeIt.gap10px,
      makeIt.centered,
      makeIt.textCentered,
      makeIt.leftAlign,
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
    ),
    ...btns.map(btn =>
      make.Div(
        makeIt.marginOnHover,
        make.Button(
          makeIt.redir,
          make.with.text(btn.text),
          make.on.click(() => {
            window.location.href = btn.loc
          })
        )
      ),
    ),
  ]
}