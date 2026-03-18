export default async () =>
{
  await import(`${window.make_url}/make.js`);

  const Style = make.style
  const makeIt = make.it
  const Paragraph = make.Paragraph
  const With = make.with

  const imp = (await import(`${window.prefab_url}/import.js`)).default(make)
  const paragraphNoticePromise = imp(`${window.prefab_url}/paragraph_notice.js`)
  const backButtonPromise = imp(`${window.prefab_url}/exit_button.js`)
  const actionNoticePromise = imp(`${window.prefab_url}/action_notice.js`)
  const popupPromise = imp(`${window.prefab_url}/popup.js`)
  const [paragraphNotice, backButton, actionNotice, popup,] = await Promise.all(
    [paragraphNoticePromise, backButtonPromise, actionNoticePromise, popupPromise]
  )
  const picButton = await imp(`${window.prefab_url}/pic_button.js`, popup, window.media_url);

  const csrfObj = await make.Query('/api/csrf-token').get()
  const qBase = make.Query("/api").via({"X-CSRFToken": csrfObj.csrfToken}).view();
  const me = await qBase.at("me").view().get()
  const qDepartments = qBase.at('departments').view()
  const qUsers = qBase.at('users').view()
  const users = await qUsers.get()
  
  const Row = (...mods) => make.Div(makeIt.flexRow, Style.gap(6), ...mods)
  const Column = (...mods) => make.Div(makeIt.flexColumn, Style.gap(6), ...mods)

  document.getElementById("left-btns").appendChild(backButton().build());

  const depsList = await qDepartments.get()
  const center = document.getElementById("center-content")

  function editActionNotice(question, cancelText, thisNotice) {
    actionNotice({
      question: question,
      action: () => make.other.closeCurrentNotice(),
      cancel: () => {
        make.other.closeCurrentNotice()
        thisNotice()
      },
      confirmText: "Закрыть",
      cancelText: cancelText,
    })
  }

  function modUserInput(inp, user, depData) {
    inp.addModifiers(
      picButton(
        "modify", "Изменить отдел", makeIt.act.alternative,
        async () => {
          let thisNotice
          let passwordField
          const deps = await qDepartments.get()
          thisNotice = async () => {
            user = await qUsers.at(user.id).view().get()
            make.Notice(
              [500, Infinity, 500, "change-dep-notice"],
              make.Div(
                makeIt.littleDarker,
                Style.padding(6),
                Style.rounded(18),
                Column(
                  makeIt.content,
                  Row(
                    picButton(
                      "close", "Закрыть меню смены отдела", makeIt.act.negative,
                      () => make.other.closeCurrentNotice()
                    ),
                    Paragraph(
                      "Выберите новый отдел:",
                      With.style({alignSelf: "center"})
                    ),
                  ),
                  make.Select(
                    make.on.change(async (e) => {
                      await qUsers.at(user.id).at("change_department").with({department: e.target.value}).view().patch()
                      user.department.id = e.target.value
                      make.other.closeCurrentNotice()
                      paragraphNotice("Отдел изменён!", make.color.yellow)
                      fillCenter(depData)
                    }),
                    ...deps.map((dep) => 
                      make.Option(
                        dep.name,
                        dep.id,
                        ...make.if(
                          dep.id === user.department.id,
                          With.attrs("selected")
                        )
                      )
                    )
                  ),
                  Column(
                    Style.padding(6),
                    Style.rounded(18),
                    make.color.lgray,
                    Paragraph("Логин:"),
                    make.Input(
                      With.attr({
                        value: user.username,
                        placeholder: user.username,
                      }),
                      make.on.input((e) => 
                        e.target.parentNode.classList.add("make-mark-changed")
                      ),
                      make.on.inputTimeOut(3000, async (e) => {
                        e.target.parentNode.classList.remove("make-mark-changed")
                        make.other.closeCurrentNotice()
                        const status = await qUsers.at(user.id).at("change_username").with({
                          username: e.target.value
                        }).on({
                          200: () => {
                            if (me.id === user.id) {
                              window.location.href = "/users/login/?next=/applications/departments-manager/"
                            }
                            editActionNotice("Успешно!", "Продолжить редактирование", thisNotice)
                          },
                          400: () => editActionNotice("Этот логин уже занят!", "Попробовать снова", thisNotice)
                        }).view().patch(true)
                      })
                    )
                  ),
                  Column(
                    Style.padding(6),
                    Style.rounded(18),
                    make.color.lgray,
                    Paragraph("Пароль:"),
                    Row(
                      passwordField = make.Input(
                        With.attr({
                          placeholder: "Запишите новый пароль для пользователя",
                        }),
                      ),
                      picButton("verify", "Подтвердить", makeIt.act.alternative,
                        async () => {
                          make.other.closeCurrentNotice()
                          const status = await qUsers.at(user.id).at("change_password").with({
                            password: passwordField.element.value
                          }).on({
                            200: () => {
                              if (me.id === user.id) {
                                window.location.href = "/users/login/?next=/applications/departments-manager/"
                              }
                              editActionNotice("Успешно!", "Продолжить редактирование", thisNotice)
                            },
                            400: () => editActionNotice("Пароль должен быть не менее 8 символов!", "Попробовать снова", thisNotice)
                          }).view().patch(true)
                        }
                      )
                    )
                  )
                )
              )
            )
          }
          thisNotice()
        }
      )
    )
  }

  let searchingElement
  async function fillCenter(depData) {
    center.innerHTML = ``
    const users = await qUsers.where({department: depData.id}).view().get()
    const scrollbox = make.Scrollbox(makeIt.flexColumn, Style.gap(6))
    if (users.length > 0) {
      center.appendChild(
        Column(
          scrollbox.addModifiers(
            ...users.map(user => {
              const inp = Input(user, qUsers, "fullname")
              modUserInput(inp, user, depData)
              return inp
            }),
          )
        ).build()
      )
      if (searchingElement) {
        for (const el of scrollbox.children) {
          if (searchingElement && el.children[0].element.value.toLowerCase().includes(searchingElement.toLowerCase())) {
            el.children[0].element.focus()
            searchingElement = null
          }
        }
      }
    }
    else {
      center.appendChild(
        Paragraph("В этом отделе нет пользователей").build()
      )
    }
  }

  function Input(fieldData, querySet, field, onClick=(()=>{})) {
    const elem = Row(makeIt.marginOnHover)
    elem.addModifiers(
      make.Input(
        With.attr({
          value: fieldData[field],
          placeholder: fieldData[field]
        }),
        make.on.click(onClick),
        make.on.input((e) => e.target.parentNode.classList.add("make-mark-changed")),
        make.on.inputTimeOut(3000, (e) => {
          if (e.target.value) {
            querySet.at(fieldData.id).with({
              [field]: e.target.value
            }).view().patch()
            e.target.parentNode.classList.remove("make-mark-changed")
            paragraphNotice("Сохранено!", make.color.green)
          }
          else {
            paragraphNotice("Невозможно сохранить отдел без имени!", make.color.red, 1500)
          }
        })
      ),
    )
    return elem
  }

  function modDepInput(inp, dep) {
    inp.addModifiers(
      picButton(
        "trash", "Удалить отдел", makeIt.act.negative,
        async () => {
          const users = await qUsers.where({department: dep.id}).view().get()
          if (users.length > 0) {
            paragraphNotice("Отдел невозможно удалить пока в нём есть сотрудники!", make.color.red, 1500)
          } else {
            actionNotice({
              confirmText: "Удалить", cancelText: "Отмена",
              question: `Удалить ${dep.name || "*безымянный отдел*"}?`,
              action: () => {
                qDepartments.at(dep.id).delete()
                inp.parent.removeChild(inp)
                paragraphNotice("Удалено!", make.color.red)
              }
            })
          }
        }
      )
    )
  }

  let scrollbox
  document.getElementById("left-content").appendChild(
    Column(
      make.Div(
        Style.rounded(6),
        make.Input(
          With.attr({
            placeholder: "Фильтр по отделу"
          }),
          make.on.input((e) => {
            for (const el of scrollbox.children) {
              if (el.children[0].element.value.toLowerCase().includes(e.target.value.toLowerCase())) {
                el.element.style.display = 'flex'
              }
              else {
                el.element.style.display = 'none'
              }
            }
          })
        ),
      ),
      make.Separator(6, Style.rounded(12), make.color.lgray),
      Style.height("100%"),
      scrollbox = make.Scrollbox(
        Style.gap(6),
        ...depsList.map((dep) => {
          const thisRow = Input(
            dep, qDepartments, "name",
            (() => async () => fillCenter(dep))()
          )
          modDepInput(thisRow, dep)
          return thisRow
        })
      ),

      make.Button(
        With.text("Добавить новый отдел"),
        makeIt.action,
        makeIt.act.positive,
        make.on.click(async () => {
          const dep = await qDepartments.with({name: "Новый пустой отдел"}).post()
          const newDep = Input(
            dep, qDepartments, "name",
            (() => async () => fillCenter(dep))()
          )
          modDepInput(newDep, dep)
          scrollbox.addChild(newDep)
          newDep.element.focus()
        })
      )
    ).build()
  )
  
  let scrollbox2
  document.getElementById("right-content").appendChild(
    Column(
      make.Div(
        Style.rounded(6),
        make.Input(
          With.attr({
            placeholder: "Поиск пользователя"
          }),
          make.on.input((e) => {
            for (const el of scrollbox2.children) {
              if (
                el.children[0].element.textContent.toLowerCase().includes(e.target.value.toLowerCase()) ||
                el.children[1].element.textContent.toLowerCase().includes(e.target.value.toLowerCase()) ||
                el.children[2].element.textContent.toLowerCase().includes(e.target.value.toLowerCase())
              ) {
                el.element.style.display = 'flex'
              }
              else {
                el.element.style.display = 'none'
              }
            }
          })
        ),
      ),
      make.Separator(6, Style.rounded(12), make.color.lgray),
      Style.height("100%"),
      scrollbox2 = make.Scrollbox(
        Style.gap(6),
        ...users.map(user => 
          make.Div(
            makeIt.flexColumn,
            makeIt.littleDarker,
            makeIt.marginOnHover,
            Style.padding(6),
            Style.rounded(12),
            Paragraph(user.fullname),
            Paragraph(user.username, makeIt.subtitleText),
            Paragraph(user.department.name, makeIt.subtitleText),
            make.on.click(() => {
              searchingElement = user.fullname
              for (const el of scrollbox.children) {
                if (el.children[0].element.value.toLowerCase().includes(user.department.name.toLowerCase())) {
                  el.children[0].element.click()
                }
              }
            })
          )
        )
      ),
    ).build()
  )

}