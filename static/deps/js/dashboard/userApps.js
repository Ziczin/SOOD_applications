export default (make) =>
async function dashboardUserApps(qBase, userId, statuses, popup, paragraphNotice) {
  const Row = (...args) => make.Div(make.it.flexRow, make.style.gap(6), ...args)
  const Column = (...args) => make.Div(make.it.flexColumn, make.style.gap(6), ...args)

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

  function redrawTabs(cards) {
    cards.forEach(card => card.parent?.detachChild(card))
    appList.children.forEach(child => appList.detachChild(child))

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
    appList.children.forEach(child => child.parent?.detachChild(child))
    appList.children = []
    const apps = await qBase.at("applications").where({
      user: userId,
      created_after: dateFrom,
      created_before: dateTo
    }).view().get()
    
    paragraphNotice(["Заявки загружены!", "Браузер занят отрисовкой, ожидайте"], make.color.green, 1000)
    appList.cards = apps.map(app => appCard(app))
    redrawTabs(appList.cards)
  }

  function setVisibilityByStatus() {
    let cards = []
    appList.cards.forEach(card => {
      if (statusSort.element.value && card.status === statusSort.element.value || !statusSort.element.value) {
        cards.push(card)
        card.element.style.display = "block"
      }
      else {
        card.element.style.display = "none"
      }
    })
    redrawTabs(cards)
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

  const sortElement = Row(
    make.with.style({flex: 0}),
    Row(
      Column(
        Row(
          make.Paragraph("Статус: ", make.with.style({alignSelf: "center"})),
          statusSort
        )
      ),
      Column(
        Row(
          make.Paragraph("от", make.with.style({alignSelf: "center"})),
          inputDateFrom
        ),
        Row(
          make.Paragraph("по ", make.with.style({alignSelf: "center"})),
          inputDateTo
        ),
      ),
    )
  )
  
  const handler = Column(
    make.style.minHeight(0),
    make.with.style({flex: 1}),
    sortElement,
    appList
  ).allowEvents().onBuild.once(getAndDraw)
  
  window.getAndDrawUserApps = getAndDraw

  function timeFormat(iso) {
    const d = new Date(iso);
    const pad = n => String(n).padStart(2, '0');
    return `${pad(d.getDate())}.${pad(d.getMonth() + 1)} `+
            `${pad(d.getHours())}:${pad(d.getMinutes())}`;
  }

  function formatYearMonth(input) {
    const [year, month] = input.split('-');
    const months = [
      'Январь','Февраль','Март','Апрель','Май','Июнь',
      'Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'
    ];
    return `${months[Number(month) - 1]} ${year}`;
  }

  function formatYearWeek(input) {
    if (!input) return ""
    const [yearPart, weekPart] = input.split('-W');
    const year = Number(yearPart);
    const week = Number(weekPart);

    function getMondayOfISOWeek(yr, wk) {
      const jan4 = new Date(Date.UTC(yr, 0, 4));
      const dayOfWeek = jan4.getUTCDay() || 7;
      const thursday = new Date(jan4);
      thursday.setUTCDate(jan4.getUTCDate() + (4 - dayOfWeek));
      const week1Monday = new Date(thursday);
      week1Monday.setUTCDate(thursday.getUTCDate() - 3);
      const targetMonday = new Date(week1Monday);
      targetMonday.setUTCDate(week1Monday.getUTCDate() + (wk - 1) * 7);
      return targetMonday;
    }

    function formatDateRus(date) {
      const dd = String(date.getUTCDate()).padStart(2, '0');
      const mm = String(date.getUTCMonth() + 1).padStart(2, '0');
      const yyyy = date.getUTCFullYear();
      return `${dd}.${mm}.${yyyy}`;
    }

    const monday = getMondayOfISOWeek(year, week);
    const sunday = new Date(monday);
    sunday.setUTCDate(monday.getUTCDate() + 6);

    return `${year}  Неделя №${week} с ${formatDateRus(monday)} по ${formatDateRus(sunday)}`;
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
    card.executor = app.executor
    let btn2
    let cardBody
    let fieldData
    card.header(
      make.with.css(`have-status-${app.status}`),
      Row(
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
      popup([
        "Нажмите чтобы увидеть подробности заявки",
        "Данные заявки подгружаются по клику, возможна небольшая задержка"
      ]),
      make.color.lgray,
      make.style.margin(-8),
      make.style.padding(6),
      make.style.rounded(12),
      make.with.style({border: "3px solid #ddd"}),
    ).content(
      make.style.height('100%'),
      cardBody = Column(
        make.Separator(),
        ...make.callif(app.executor !== null,
          () => Row(
            make.it.marginOnHover,
            make.Paragraph(`Исполнитель: ${app.executor.fullname}`),
            make.Paragraph(`(${app.executor.department.name})`, make.it.subtitleText),
          ),
        ),
        fieldData = Column(),
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
                qBase.at("applications").at(app.id).with({
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
                  Column(
                    make.it.contented,
                    make.Paragraph("Для отмены заявки укажите причину:"),
                    inp,
                    Row(
                      make.Button(
                        make.it.action,
                        make.it.act.negative,
                        make.with.text("Отменить"),
                        make.with.style({flex: 1}),
                        make.on.click(async () => {
                          if (inp.element.value) {
                            qBase.at("applications").at(app.id).with({
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
    setStatusStyle(card.cardHeader.element, app.status)
    card.cardBody = cardBody
    card.allowCustomEvents()
    
    app.application_fields.forEach(field => {
      if (!field.value) {
        fieldData.addChild(
          Row(
            make.it.marginOnHover,
            make.Paragraph(`${field.label}: <<< не указано >>>`),
            make.it.subtitleText
          )
        )
      }
      else {
        if (field.type.name === "textarea") {
          fieldData.addChild(
            make.Card(
              make.it.littleDarker,
              make.style.rounded(12),
              make.style.padding(4)
            )
            .header(make.Paragraph(field.label))
            .content(make.Paragraph(field.value))
          )
        }
        else {
          let value = field.value
          if (field.type.name === "datetime") {
            value = field.value.replace(/T/g, ' ');
          }
          if (field.type.name === "month") {
            value = formatYearMonth(field.value)
          }
          if (field.type.name === "week") {
            value = formatYearWeek(field.value)
          }
          if (field.type.name === "checkbox") {
            value = field.value === 'on' ? "Да" : "Нет"
          }
          fieldData.addChild(
            Row(
              make.it.marginOnHover,
              make.Paragraph(`${field.label}: ${value}`),
              ...make.if(field.tag !== null,
                make.Paragraph(`(${field.tag})`, make.it.subtitleText),
              ),
            )
          )
        }
      }
    })
    
    card.btn2 = btn2
    return card
  }

  function addApplication(app) {
    const card = appCard(app);
    if (appList.cards) {
      appList.cards.unshift(card);
      setVisibilityByStatus();
    }
  }

  qBase.at("events").at("check").with(
    {user_id: userId, event: "application-status-change-userboard", other: userId}
  ).view().repeat(
    1000, 'POST', (resp)=> {
      appList.cards.forEach((card) => {
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

  return {
    handler: handler,
    addApplication: addApplication,
    getAndDraw: getAndDraw
  }
}