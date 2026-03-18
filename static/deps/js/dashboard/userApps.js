export default (make) =>
async function dashboardUserApps(qBase, userId, statuses, popup, paragraphNotice) {
  const Style = make.style
  const Paragraph = make.Paragraph
  const With = make.with
  const makeIt = make.it
  const Row = (...args) => make.Div(makeIt.flexRow, Style.gap(6), ...args)
  const Column = (...args) => make.Div(makeIt.flexColumn, Style.gap(6), ...args)

  const appList = make.Scrollbox(
    makeIt.flexColumn,
    Style.height("100%"),
    Style.gap(6),
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
      Style.margin(8),
      makeIt.flexColumn,
    ).menu(
      Style.padding(8),
      Style.rounded(12),
      makeIt.flexRow,
      With.style({flex: "0 0 auto"}),
      Style.gap(8)
    ).content(
      makeIt.flexColumn
    )
    let pageCounter = 0
    let pageCards = []
    cards.forEach((card, index) => {
      pageCards.push(card)
      if (pageCards.length >= 20 || cards.length === index + 1) {
        pageCounter++
        tabs.tab()
        .header(
          Style.rounded(12),
          Style.padding(8),
          makeIt.centered,
          makeIt.textCentered,
          Paragraph(`${pageCounter}`)
        ).content(
          makeIt.flexColumn,
          With.style({flex: "1 1 auto"}),
          Style.gap(6),
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
    With.attr({type: "date", value: formatDateForInput(weekAgo)}),
    make.on.change(getAndDraw),
    popup([
      "Дата начала выборки",
      "Как только вы смените дату, сервис повторно загрузит ваши заявки за данный период",
      "Это может занять некоторое время, если выбранный период будет слишком большим"
    ])
  )

  const inputDateTo = make.Input(
    With.attr({type: "date", value: formatDateForInput(today)}),
    make.on.change(getAndDraw),
    popup([
      "Дата конца выборки",
      "Как только вы смените дату, сервис повторно загрузит ваши заявки за данный период",
      "Это может занять некоторое время, если выбранный период будет слишком большим"
    ])
  )

  const sortElement = Row(
    With.style({flex: 0}),
    Row(
      Column(
        Row(
          Paragraph("Статус: ", With.style({alignSelf: "center"})),
          statusSort
        )
      ),
      Column(
        Row(
          Paragraph("от", With.style({alignSelf: "center"})),
          inputDateFrom
        ),
        Row(
          Paragraph("по ", With.style({alignSelf: "center"})),
          inputDateTo
        ),
      ),
    )
  )
  
  const handler = Column(
    Style.minHeight(0),
    With.style({flex: 1}),
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
      makeIt.marginOnHover,
      With.style({border: "3px solid #ddd", backgroundColor: "#f5f5f5"}),
      Style.padding(6),
      Style.rounded(12),
    )
    card.status = app.status
    card.id = app.id
    card.executor = app.executor
    let btn2
    let cardBody
    let fieldData
    card.header(
      With.css(`have-status-${app.status}`),
      Row(
        make.Div(
          makeIt.flexRow,
          Style.gap(9),
          With.style({alignSelf: "center"}),
          Paragraph(`№ ${app.id}`, makeIt.textBold, With.style({flex: "0 1 auto"})),
          Paragraph(
            `${timeFormat(app.date)} -`,
            With.style({flex: "0 1 auto"}),
          ),
          Paragraph(app.form.label)
        ),
      ),
      popup([
        "Нажмите чтобы увидеть подробности заявки",
        "Данные заявки подгружаются по клику, возможна небольшая задержка"
      ]),
      make.color.lgray,
      Style.margin(-8),
      Style.padding(6),
      Style.rounded(12),
      With.style({border: "3px solid #ddd"}),
    ).content(
      Style.height('100%'),
      cardBody = Column(
        make.Separator(),
        ...make.callif(app.executor !== null,
          () => Row(
            makeIt.marginOnHover,
            Paragraph(`Исполнитель: ${app.executor.fullname}`),
            Paragraph(`(${app.executor.department.name})`, makeIt.subtitleText),
          ),
        ),
        fieldData = Column(),
        ...make.if(app.msg,
          Paragraph(
            app.status === "REJECTED"
            ? `Причина отказа: ${app.msg}`
            : app.status === "CANCELLED"
            ? `Причина отмены: ${app.msg}`
            : "Этой надписи тут быть не должно - обратитесь в отдел программирования",
            makeIt.marginOnHover
          )
        ),
        ...make.if(
          ["SENDED", "IN_PROGRESS"].includes(card.status),
          btn2 = make.Button(
            With.text("Отменить"),
            makeIt.action,
            makeIt.act.negative,
            Style.padding(3),
            Style.margin(-2),
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
                const inp = make.TextArea(
					With.style({
						resize: "vertical"
					})
				)
                make.Notice([500, Infinity, 500, "actionNotice"],
                  Column(
                    makeIt.contented,
                    Paragraph("Для отмены заявки укажите причину:"),
                    inp,
                    Row(
                      make.Button(
                        makeIt.action,
                        makeIt.act.negative,
                        With.text("Отменить"),
                        With.style({flex: 1}),
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
                              Paragraph(`Причина отмены: ${inp.element.value}`)
                            )
                            make.other.closeCurrentNotice()
                          }
                        })
                      ),
                      make.Button(
                        makeIt.action,
                        makeIt.act.alternative,
                        With.text("Не отменять"),
                        With.style({flex: 1}),
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
            makeIt.marginOnHover,
            Paragraph(`${field.label}: <<< не указано >>>`),
            makeIt.subtitleText
          )
        )
      }
      else {
        if (field.type.name === "textarea") {
          fieldData.addChild(
            make.Card(
              makeIt.littleDarker,
              Style.rounded(12),
              Style.padding(4)
            )
            .header(Paragraph(field.label))
            .content(Paragraph(field.value))
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
              makeIt.marginOnHover,
              Paragraph(`${field.label}: ${value}`),
              ...make.if(field.tag !== null,
                Paragraph(`(${field.tag})`, makeIt.subtitleText),
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
            make.Separator(4, Style.rounded(12), make.color.lgray),
          )
          if (resp.msg) {
            card.cardBody.addChild(
              make.Div(
                makeIt.marginOnHover,
                Paragraph(resp.status === "REJECTED"
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
                  makeIt.marginOnHover,
                  Paragraph(`Исполнитель: ${resp.executor}`),
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