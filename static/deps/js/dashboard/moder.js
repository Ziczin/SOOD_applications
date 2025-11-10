export default (make) =>
async function dashboardModer(qBase, department, statuses, popup, onOpenFooContainer, me, paragraphNotice) {
  onOpenFooContainer.push(getAndDraw)
  const appList = make.Scrollbox(
    make.it.flexColumn,
    make.style.maxWidth('100%'),
    make.style.gap(6),
  )

  function redrawTabs(cards) {
    appList.children.forEach(child => appList.removeChild(child))
    appList.children = []

    const tabs = make.Tabs(
      {scroll: true, noAnimation: true, squareTabs: true},
      make.style.margin(8),
      make.it.flexColumn,
    ).menu(
      make.style.padding(8),
      make.style.rounded(12),
      make.it.flexRow,
      make.with.style({flex: "0 0 auto"}),
      make.style.gap(8)
    ).content(
      make.it.flexColumn
    )
    let pageCounter = 0
    let pageCards = []
    cards.forEach((card, index) => {
      pageCards.push(card)
      if (pageCards.length >= 20 || cards.length === index + 1) {
        pageCounter++
        tabs.tab()
        .header(
          make.style.rounded(12),
          make.style.padding(8),
          make.it.centered,
          make.it.textCentered,
          make.Paragraph(`${pageCounter}`)
        ).content(
          make.it.flexColumn,
          make.with.style({flex: "1 1 auto"}),
          make.style.gap(6),
          ...pageCards
        )
        pageCards = []
      }
    })
    appList.addChild(tabs)
    appList.build()
  }
  async function fillApps(dateFrom, dateTo) {
    paragraphNotice(["Заявки загружаются", "Это может занять некоторое время"], make.color.yellow, 2500)
    const apps = await qBase.at("applications").where({
      department: department,
      created_after: dateFrom,
      created_before: dateTo,
      short: true
    }).view().get()
    paragraphNotice(["Заявки загружены!", "Браузер занят отрисовкой, ожидайте"], make.color.green, 1000)
    appList.cards = apps.map((app) => appCard(app))
    redrawTabs(appList.cards)
  }
  function setVisibilityByStatus() {
    let cards = []
    appList.cards.forEach(card => {
      const matchStatus = statusSort.element.value === card.status
      const sended = card.status === "SENDED"
      const in_progress = card.status === "IN_PROGRESS"
      const completed = card.status === "COMPLETED"
      const rejected = card.status === "REJECTED"
      const bntBuilded = card.element && card.btnProc && card.btnProc.element
      if (card.element) {
        if (!matchStatus) card.element.style.display = "none"
        else {
          cards.push(card)
          card.element.style.display = "block"
          if (bntBuilded) {
            if (completed || rejected) {
              card.btnProc.parent.removeChild(card.btnProc)
              card.btnCanc.parent.removeChild(card.btnCanc)
              card.btnHolder.parent.removeChild(card.btnHolder)
            }
            else if (sended) card.btnProc.element.textContent = "Принять"
            else if (in_progress) card.btnProc.element.textContent = "Завершить"
          }
        }
      }
    })
    redrawTabs(cards)
  }
  const statusSort = make.Select(
    ...statuses.map(status => make.Option(status.label, status.key)),
    make.on.change(setVisibilityByStatus)
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
    make.on.change(getAndDraw)
  )

  const inputDateTo = make.Input(
    make.with.attr({type: "date", value: formatDateForInput(today)}),
    make.on.change(getAndDraw)
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
    ),
    make.SideSeparator(12),
    make.Div(
      make.it.flexRow,
      make.style.gap(6),
      make.Paragraph("с ", make.with.style({alignSelf: "center"})),
      inputDateFrom,
      make.SideSeparator(12),
      make.Paragraph("по ", make.with.style({alignSelf: "center"})),
      inputDateTo
    )
  )
  const handler = make.Div(
    make.it.flexColumn,
    make.style.gap(6),
    make.style.maxWidth('100%'),
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
    )
    card.status = app.status
    card.id = app.id
    let btnProc
    let btnCanc
    let cardBody
    let btnHolder
    let fieldData
    card.header(
      make.Div(
        make.it.flexRow,
        make.style.gap(6),
        make.Div(
          make.it.flexRow,
          make.style.gap(9),
          make.with.style({alignSelf: "center"}),
          make.Paragraph(`№ ${app.id}`, make.it.textBold, make.with.style({flex: "0 1 auto"})),
          make.Paragraph(
            `${timeFormat(app.date)} -`,
            make.with.style({flex: "0 1 auto"}),
          ),
          make.Paragraph(app.form.label)
        ),
      ),
      popup("Нажмите чтобы развернуть заявку"),
      make.color.lgray,
      make.style.margin(-8),
      make.style.padding(6),
      make.style.rounded(12),
      make.with.style({border: "3px solid #ddd"}),
    ).content(
      make.Separator(6),
      make.style.height('100%'),
      cardBody = make.Div(
        make.it.flexColumn,
        make.style.gap(6),
        make.Separator(),
        make.Div(
          make.it.flexRow,
          make.style.gap(6),
          make.it.marginOnHover,
          make.Paragraph(`От: ${app.user.fullname}`),
          make.callif(app.user.department,
            () => make.Paragraph(`(${app.user.department.name})`, make.it.subtitleText),
          ),
        ),
        ...make.callif(app.executor !== null,
          () => make.Paragraph(`Исполнитель: ${app.executor.fullname}`,
            make.it.marginOnHover
          )
        ),
        make.Separator(2, make.color.lgray),
        fieldData = make.Div(
          make.it.flexColumn,
          make.style.gap(6)
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
          ["SENDED", "IN_PROGRESS"].includes(card.status)
          && (app.executor === null || app.executor.id === me.id),
          btnHolder = make.Div(
            make.it.flexRow,
            make.style.gap(6),
            make.style.margin(2),
            btnProc = make.Button(
              make.with.style({flex: 1}),
              make.with.text("placeholder"),
              make.it.action,
              make.it.act.positive,
              make.style.padding(3),
              make.style.margin(-2),
              make.on.click(async (e) => {
                e.stopPropagation();
                const newStatus = card.status === "SENDED" ? "IN_PROGRESS" : "COMPLETED"
                await qBase.at("applications").at(app.id).with({
                  status: newStatus,
                  executor: me.id
                }).view().patch()
                card.status = newStatus
                if (card.status === "COMPLETED")
                  btnProc.element.display = "none"
                setVisibilityByStatus()
              })
            ),
            btnCanc = make.Button(
              make.with.style({flex: 1}),
              make.with.text("Отклонить"),
              make.it.action,
              make.it.act.negative,
              make.style.padding(3),
              make.style.margin(-2),
              make.on.click(async (e) => {
                e.stopPropagation();
                const inp = make.Input()
                make.Notice([500, Infinity, 500, "actionNotice"],
                  make.Div(
                    make.it.flexColumn,
                    make.style.gap(6),
                    make.it.contented,
                    make.Paragraph("Для того чтобы отказать в заявке укажите причину отказа:"),
                    inp,
                    make.Div(
                      make.it.flexRow,
                      make.style.gap(6),
                      make.Button(
                          make.it.action,
                          make.it.act.negative,
                          make.with.text("Отказать"),
                          make.with.style({flex: 1}),
                          make.on.click(async () => {
                            if (inp.element.value) {
                              await qBase.at("applications").at(app.id).with({
                                status: "REJECTED",
                                msg: inp.element.value,
                                executor: me.id
                              }).view().patch()
                              card.status = "REJECTED"
                              setVisibilityByStatus()
                              card.btnProc.destroy()
                              card.btnCanc.destroy()
                              card.btnHolder.destroy()
                              cardBody.addChild(
                                make.Paragraph(
                                  `Причина отказа: ${inp.element.value}`,
                                  make.it.marginOnHover
                                )
                              )
                              make.other.closeCurrentNotice()
                            }
                          })
                      ),
                      make.Button(
                        make.it.action,
                        make.it.act.alternative,
                        make.with.text("Отмена"),
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
        ),
          
      )
    )
    card.cardBody = cardBody
    card.allowCustomEvents()
    async function drawFields()
    {
      const _app = await qBase.at("applications").at(app.id).view().get()
      _app.application_fields.forEach(field => 
        fieldData.addChild(
          make.Div(
            make.it.flexRow,
            make.style.gap(6),
            make.it.marginOnHover,
            make.Paragraph(`${field.label}: ${field.value}`),
            ...make.if(field.tag !== null,
              make.Paragraph(`(${field.tag})`, make.it.subtitleText),
            )
          )
        )
      )
      card.onOpenStart.unsub(drawFields)
    }
    card.onOpenStart.sub(drawFields)
    card.btnProc = btnProc
    card.btnCanc = btnCanc
    card.btnHolder = btnHolder
    return card
  }

  qBase.at("events").at("check").with(
    {user_id: me.id, event: "application-appear", other: me.department.id}
  ).view().repeat(
    1000, 'POST', (resp)=> {
      if (appList.cards) {
        appList.cards.unshift(appCard(resp))
        setVisibilityByStatus()
      }
      paragraphNotice(
        [`${resp.form.label} № ${resp.id}`, `От ${resp.user.fullname}`],
        make.color.yellow, 2500, false
      )
    }
  )
  qBase.at("events").at("check").with(
    {user_id: me.id, event: "application-status-change-moderboard", other: department}
  ).view().repeat(
    1000, 'POST', (resp)=> {
      appList.cards.forEach((card) => {
        if (card.id === resp.id) {
          card.status = resp.status
          card.cardBody.addChild(
            make.Separator(4, make.style.rounded(12), make.color.lgray),
          )
          if (resp.msg) {
            card.cardBody.addChild(
              make.Div(
                make.it.marginOnHover,
                make.Paragraph(`Причина: ${resp.msg}`),
              )
            )
          }
          else {
            card.cardBody.addChild(
              make.Div(
                make.it.marginOnHover,
                make.Paragraph(`Исполнитель: ${resp.executor}`),
              )
            )
          }
          
          card.removeChild(card.btnCanc)
          card.btnCanc.destroy()
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
        make.color.blue, 2500, false
      )
    }
  )
  return [handler]
}