export default (make) =>
async function dashboardUserApps(qBase, userId, statuses, popup, paragraphNotice) {
  const appList = make.Scrollbox(
    make.it.flexColumn,
    make.style.height("100%"),
    make.style.gap(6),
  )

  function setStatusStyle(element, style) {
    if (!element || typeof element.className !== 'string') return;
    element.className = element.className
      .split(/\s+/)
      .filter(function(c) { return c.indexOf('have-status-') !== 0; })
      .join(' ')
      .trim();
    if (style && style.toString().trim() !== '') {
      var newClass = 'have-status-' + style;
      if (element.className) element.className += ' ' + newClass;
      else element.className = newClass;
    }
  }

  async function fillApps(dateFrom, dateTo) {
    appList.children.forEach(child => appList.removeChild(child))
    appList.children = []
    const apps = await qBase.at("applications").where({
      user: userId,
      created_after: dateFrom,
      created_before: dateTo
    }).view().get()
    
    apps.forEach(app => {
      const card = appCard(app)
      appList.addChild(card)
    })
  }

  function setVisibilityByStatus() {
    appList.children.forEach(card => {
      if (statusSort.element.value && card.status === statusSort.element.value || !statusSort.element.value) {
        card.element.style.display = "block"
      }
      else {
        card.element.style.display = "none"
      }
    })
    appList.build()
  }

  const statusSort = make.Select(
    make.OptionPlaceholder("Все"),
    ...statuses.map(status => make.Option(status.label, status.key)),
    make.on.change(setVisibilityByStatus),
    popup(["Укажите статус", "Сервис отсортирует все ваши заявки по указанному статусу"])
  )

  function formatDateForInput(date){
    const y = date.getFullYear();
    const m = String(date.getMonth()+1).padStart(2,'0');
    const d = String(date.getDate()).padStart(2,'0');
    return `${y}-${m}-${d}`;
  }

  const today = new Date();
  const weekAgo = new Date();
  weekAgo.setDate(today.getDate() - 7);

  async function getAndDraw() {
    await fillApps(inputDateFrom.element.value, inputDateTo.element.value)
    setVisibilityByStatus()
  }

  const inputDateFrom = make.Input(
    make.with.attr({type: "date", value: formatDateForInput(weekAgo)}),
    make.on.change(getAndDraw),
    popup([
      "Дата начала выборки",
      "Как только вы смените дату, сервис повторно загрузит ваши заявки за данный период",
      "Это может занять некоторое время, если выбранный период будет слишком большим"
    ])
  )

  const inputDateTo = make.Input(
    make.with.attr({type: "date", value: formatDateForInput(today)}),
    make.on.change(getAndDraw),
    popup([
      "Дата конца выборки",
      "Как только вы смените дату, сервис повторно загрузит ваши заявки за данный период",
      "Это может занять некоторое время, если выбранный период будет слишком большим"
    ])
  )

  const sortElement = make.Div(
    make.it.flexRow,
    make.style.gap(6),
    make.with.style({flex: 0}),
    make.Div(
      make.it.flexRow,
      make.style.gap(6),
      make.Paragraph("Статус: ", make.with.style({alignSelf: "center"})),
      statusSort,
      make.Paragraph(" с", make.with.style({alignSelf: "center"})),
      inputDateFrom,
      make.Paragraph("по", make.with.style({alignSelf: "center"})),
      inputDateTo
    )
  )
  
  const handler = make.Div(
    make.it.flexColumn,
    make.style.gap(6),
    make.style.minHeight(0),
    make.with.style({flex: 1}),
    sortElement,
    appList
  )

  function timeFormat(iso) {//.${d.getFullYear()}
    const d = new Date(iso);
    const pad = n => String(n).padStart(2, '0');
    return `${pad(d.getDate())}.${pad(d.getMonth() + 1)} `+
            `${pad(d.getHours())}:${pad(d.getMinutes())}`;
  }

  function appCard(app) {
    const card = make.Card(
      make.it.marginOnHover,
      make.with.style({border: "3px solid #ddd", backgroundColor: "#f5f5f5"}),
      make.style.padding(6),
      make.style.rounded(12),
      popup(400, "Нажмите, чтобы раскрыть подробности")
    )
    card.status = app.status
    card.id = app.id
    card.executor = app.executor
    let btn2
    let cardBody
    card.header(
      make.with.css(`have-status-${app.status}`),
      make.Div(
        make.it.flexRow,
        make.style.gap(6),
        make.Div(
          make.it.flexRow,
          make.style.gap(9),
          make.with.style({alignSelf: "center"}),
          make.Paragraph(`№ ${app.id}`, make.it.textBold, make.with.style({flex: "0 1 auto"})),
          make.Paragraph(timeFormat(app.date), make.with.style({flex: "1 1 auto"})),
          make.Paragraph(app.form.label, make.with.style({flex: "100 1 auto"}))
        ),
      ),
      popup("Нажмите чтобы развернуть заявку"),
      make.color.lgray,
      make.style.margin(-8),
      make.style.padding(6),
      make.style.rounded(12),
      make.with.style({border: "3px solid #ddd"}),
    ).content(
      make.style.height('100%'),
      cardBody = make.Div(
        make.it.flexColumn,
        make.style.gap(6),
        make.Separator(),
        ...make.callif(app.executor !== null,
          () => make.Div(
            make.it.flexRow,
            make.style.gap(6),
            make.it.marginOnHover,
            make.Paragraph(`Исполнитель: ${app.executor.fullname}`),
            make.Paragraph(`(${app.executor.department.name})`, make.it.subtitleText),
          ),
        ),
        make.Separator(4, make.style.rounded(12), make.color.lgray),
        ...app.application_fields.map(field => 
          make.Div(
            make.it.flexRow,
            make.style.gap(6),
            make.it.marginOnHover,
            make.Paragraph(`${field.label}: ${field.value}`),
            ...make.if(field.tag !== null,
              make.Paragraph(`(${field.tag})`, make.it.subtitleText),
            )
          )
        ),
        ...make.if(app.msg,
          make.Paragraph(
            app.status === "REJECTED"
            ? `Причина отказа: ${app.msg}`
            : app.status === "CANCELLED"
            ? `Причина отмены: ${app.msg}`
            : "Этой надписи тут быть не должно - обратитесь в отдел программирования",
            make.it.marginOnHover
          )
        ),
        ...make.if(
          ["SENDED", "IN_PROGRESS"].includes(card.status),
          btn2 = make.Button(
            make.with.text("Отменить"),
            make.it.action,
            make.it.act.negative,
            make.style.padding(3),
            make.style.margin(-2),
            popup([
              "Нажмите чтобы отменить заявку",
              "Отменить заявку можно только если она не была принята в работу"
            ]),
            ...make.if(card.status === "SENDED",
              make.on.click(async (e) => {
                e.stopPropagation()
                await qBase.at("applications").at(app.id).with({
                  status: "CANCELLED",
                }).view().patch()
                card.status = "CANCELLED"
                setStatusStyle(card.cardHeader.element, card.status)
                setVisibilityByStatus()
                card.btn2.destroy()
              })
            ),
            ...make.if(card.status === "IN_PROGRESS",
              make.on.click(async (e) => {
                e.stopPropagation();
                const inp = make.Input()
                make.Notice([500, Infinity, 500, "actionNotice"],
                  make.Div(
                    make.it.flexColumn,
                    make.style.gap(6),
                    make.it.contented,
                    make.Paragraph("Для отмены заявки укажите причину:"),
                    inp,
                    make.Div(
                      make.it.flexRow,
                      make.style.gap(6),
                      make.Button(
                        make.it.action,
                        make.it.act.negative,
                        make.with.text("Отменить"),
                        make.with.style({flex: 1}),
                        make.on.click(async () => {
                          if (inp.element.value) {
                            await qBase.at("applications").at(app.id).with({
                              status: "CANCELLED",
                              executor: userId,
                              msg: inp.element.value
                            }).view().patch()
                            card.status = "CANCELLED"
                            setStatusStyle(card.cardHeader.element, card.status)
                            setVisibilityByStatus()
                            card.btn2.destroy()
                            cardBody.addChild(
                              make.Paragraph(`Причина отмены: ${inp.element.value}`)
                            )
                            make.other.closeCurrentNotice()
                          }
                        })
                      ),
                      make.Button(
                        make.it.action,
                        make.it.act.alternative,
                        make.with.text("Не отменять"),
                        make.with.style({flex: 1}),
                        make.on.click(() => {
                          make.other.closeCurrentNotice()
                        })
                      ),
                    )
                  )
                )
              })
            )
          )
        )
      )
    )
    card.btn2 = btn2
    card.cardBody = cardBody

    return card
  }

  handler.allowEvents()
  handler.onBuild.sub(async () => {
    await getAndDraw()
    handler.onBuild.unsub(getAndDraw)
  })
  window.getAndDrawUserApps = getAndDraw

  qBase.at("events").at("check").with(
    {user_id: userId, event: "application-status-change-userboard", other: userId}
  ).view().repeat(
    1000, 'POST', (resp)=> {
      appList.children.forEach((card) => {
        if (card.id === resp.id) {
          card.status = resp.status
          setStatusStyle(card.cardHeader.element, card.status)
          card.cardBody.addChild(
            make.Separator(4, make.style.rounded(12), make.color.lgray),
          )
          if (resp.msg) {
            card.cardBody.addChild(
              make.Div(
                make.it.marginOnHover,
                make.Paragraph(resp.status === "REJECTED"
                ? `Причина отказа: ${resp.msg}`
                : resp.status === "CANCELLED"
                ? `Причина отмены: ${resp.msg}`
                : "Этой надписи тут быть не должно - обратитесь в отдел программирования",),
              )
            )
            card.msg = resp.msg
          }
          else {
            if (!card.executor && resp.executor) {
              card.cardBody.addChild(
                make.Div(
                  make.it.marginOnHover,
                  make.Paragraph(`Исполнитель: ${resp.executor}`),
                )
              )
              card.executor = resp.executor
            }
          }
          
          card.removeChild(card.btn2)
          card.btn2.destroy()
        }
      })
      setVisibilityByStatus()
      paragraphNotice(
        ["Изменён статус по заявке",
          `${resp.form} №${resp.id}`,
          `Исполнитель: ${resp.executor}`,
          `Статус: ${resp.status}`,
          resp.msg && `Сообщение: ${resp.msg}`,
        ],
        make.color.yellow, 2500, false
      )
    }, 401
  )
  return handler
}