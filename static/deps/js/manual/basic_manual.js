export default (make, popup, picButton) => (additionalContent) => {
  function manualHeader() {
    let styleTab = [make.style.padding(4), make.style.rounded(4)]
    return [
      make.Div(
        make.it.flexRow, make.style.gap(6), make.style.maxHeight("10%"),
        manualCloseText(),
        make.h1("Руководство"),
      ),
      make.Separator(6),
      ...make.if(additionalContent,
        make.Tabs()
        .menu(make.style.gap(6), make.style.rounded(8), make.style.padding(4))
        .content(make.style.maxHeight("auto"), make.style.padding(0), make.Separator(6))
        .tab()
        .header(...styleTab, make.Paragraph("Общие положения"))
        .content(manualBaseTabs(true))
        .tab()
        .header(...styleTab, make.Paragraph("О странице"))
        .content(additionalContent)
      ),
      ...make.if(!additionalContent,
        manualBaseTabs(false)
      )
    ]
  }

  function manualBaseTabs(isAddit) {
    let styleTab = [make.style.padding(4), make.style.rounded(4)]
    return make.Tabs(
      make.style.width("100%"),
      make.style.height("100%"),
    )
    .menu(make.style.gap(6), make.style.rounded(8), make.style.padding(4))
    .content(make.style.maxHeight("auto"))
    .tab()
    .header(...styleTab, make.Paragraph("Главная"))
    .content(
      make.style.maxHeight("100%"),
      make.it.flexColumn, make.style.gap(6),
      make.Paragraph("• Это руководство кратко описывает функциональные возможности разных менеджеров"),
      ...make.if(isAddit,
        make.Paragraph(`• Вы находитесь на вкладке "Общие положения"`),
        make.Paragraph("• Выше, находятся вкладки, на которых расписан основной функционал"),
      ),
      make.Paragraph("• Руководство предназначено для тех, кто в отделе был назначен администратором"),
      make.Paragraph("• Пишите в отдел программирования если остался вопрос, на который в данном руководстве нет ответа"),
      make.Separator(0),
      make.Paragraph(`Можете перейти на вкладку "Подсказки"`),
      sideParagraphWithMargin("Если вас не устраивает размер текста, то вы можете изменить его сами, " +
        "используя страндартные инструменты браузера: CTRL + \"+\" для увеличения размера элементов, " +
        "CTRL + \"-\" для уменьшения размера элементов", make.it.subtitleText),
    )
    .tab()
    .header(...styleTab, make.Paragraph("Подсказки"))
    .content(
      make.it.flexColumn, make.style.gap(6),
      make.Paragraph("• Большая часть элементов при наведении выведет вам подсказку через 1.5 секунды"),
      make.Paragraph("Наведитесь на эту строку и подождите несколько секунд", make.with.style({textDecoration: "underline"}),
      popup(
        "Так будет выглядить подсказка",
        "Зачастую, в подсказках будут проянены некоторые моменты",
        "которые могут показаться неочевидными на первый взгляд"
      ),
      make.on.click((e) => {
        e.target.textContent = "НЕ НУЖНО НАЖИМАТЬ, ПРОСТО НАВЕДИТЕСЬ";
      })),
      make.Separator(),
      make.Paragraph("• Подсказки могут быть не только над текстом, но и над элементами"),
      make.Paragraph("• Ниже находятся различные элементы. Наведитесь на любой из них и подождите несколько секунд"),
      make.Div(
        make.it.flexRow,
        make.style.gap(6),
        make.Input(make.with.attr({placeholder: "Это поле ввода"}),
          popup(800, "Это подсказка на поле ввода"), make.style.maxWidth("20%"),
        ),
        make.Input(make.with.attr({placeholder: "Это поле ввода отключено", disabled: ""}),
          popup(800, "Это подсказка на поле ввода",
            "подсказки могут находиться на элементах, даже если те отключены"
          )
        ),
        make.Button(make.it.redir, make.with.text("это кнопка"),
          popup(800, "Это подсказка на кнопке"), make.with.style({whiteSpace: "nowrap"}),
          make.on.click((e) => e.target.textContent = "Тут нет ничего интересного")
        ),
        make.Div(
          make.it.flexRow,
          make.style.gap(6),
          make.style.minWidth("24%"),
          picButton("save", `Это подсказка на кнопке "Сохранить"`),
          picButton("verify", `Это подсказка на кнопке "Верифицировать"`),
          picButton("hide", `Это подсказка на кнопке "Скрыть/Показать"`),
          picButton("share", `Это подсказка на кнопке "Поделиться"`),
          picButton("trash", `Это подсказка на кнопке "Удалить"`),
          picButton("close", `Это подсказка на кнопке "Закрыть"`),
        )
      ),
      make.Separator(),
      make.Paragraph("• Список элементов не ограничивается кнопками и полями ввода"),
      make.Separator(),
      make.Paragraph(`Можете перейти на вкладку "Кнопки управления"`)
    )
    .tab()
    .header(...styleTab, make.Paragraph("Кнопки управления"))
    .content(
      make.it.flexColumn, make.style.gap(6),
      make.Paragraph("• Кнопки управления позволяют взаимодействовать с ближайшим элементом"),
      make.Paragraph("• Если на одной строке содержатся кнопки и поле ввода, то все кнопки относятся к этому полю ввода"),
      make.Paragraph("• Кнопки имеют смысл в контексте того, где они находятся, наведитесь на них чтобы увидеть описание их действий"),
      make.Separator(0),
      make.Paragraph("• Разберём что из себя представляют кнопки управления в общем случае:"),
      make.Div(
        make.it.flexColumn, make.style.gap(6),
        manualFunctionalButtonElement(
          "save", [`"Дискета"`, "Сохранить"], make.it.act.positive,
          "Кнопки с изображением дискеты обычно сохраняют данные или фиксируют изменения",
        ),
        manualFunctionalButtonElement(
          "verify", [`"Галочка"`, "Подтвердить"], make.it.act.positive,
          "Кнопки с изображением галочки обычно подтвержают или разрешают что-то",
        ),
        manualFunctionalButtonElement(
          "hide", [`"Глаз"`, "Скрыть/показать"], make.it.act.alternative,
          "Кнопки с изображением глаза обычно скрывают или раскрывают данные"
        ),
        manualFunctionalButtonElement(
          "share", [`"Граф"`, "Поделиться"], make.it.act.neutral,
          "Кнопки с изображением графа обычно означают что этим элементом можно поделиться",
        ),
        manualFunctionalButtonElement(
          "trash", [`"Корзина"`, "Удалить"], make.it.act.negative,
          "Кнопки с изображением корзины обычно удаляют данные",
        ),
        manualFunctionalButtonElement(
          "close", [`"Крестик"`, "Закрыть"], make.it.act.negative,
          "Кнопки с изображением крестика обычно закрывают текущее окно",
        ),
      ),
      make.Paragraph("Можете перейти на вкладку \"Быстрая навигация\"")
    )
    .tab()
    .header(...styleTab, make.Paragraph("Быстрая навигация"))
    .content(
      make.it.flexColumn, make.style.gap(6),
      make.Paragraph(
        "• Менеждер перечислений построент так, чтобы добавление " + 
        "новых элементов не занимало много времени"),
      make.Paragraph(
        "• При добавлении нового элемента, менеджер перечислений автоматически " +
        "переключается на него и вы можете не выбирать его вручную каждый раз"),
      make.Separator(),
      make.Paragraph("Почему это сделано именно так:"),
      sideParagraphWithMargin(
        "Клавиша TAB на вашей клавиатуре позволяет выбрать следующий элемент на странице"),
      sideParagraphWithMargin("Сочетание клавиш SHIFT + TAB возвращает выделение на предыдущий элемент"),
      sideParagraphWithMargin("Клавиша ПРОБЕЛ, в свою очередь, работает как клик мышкой " +
          "для элементов, которые были выбраны при помощи TAB"),
      sideParagraphWithMargin("Сочетание клавиш SHIFT + ПРОБЕЛ, так же работает как клик мышкой, " +
          "поэтому можно не отпускать SHIFT, если пролистываете выделеные элементы в обратную сторону"),
      make.Separator(),
      make.Paragraph("• Попробуйте отключить видимость у всех полей, " +
        "не нажимая мышкой по кнопке \"Скрыть/показать\""),
      ...[1,2,3,4].map((i)=>
        inputFull({id: 0, value: `Поле №${i}`, visible: true, test: true}),
      ),
      make.Paragraph("Нажмите на первое поле ввода и нажимайте TAB, " +
        "пока не окажитесь на нужной кнопке, после чего нажмите ПРОБЕЛ", make.it.subtitleText),
    )
  }

  function manualFunctionalButtonElement(pic, popup, styles, t1, t2) {
    return make.Div(
      make.it.flexRow,
      make.style.gap(6),
      make.style.padding(6),
      make.it.marginOnHover,
      make.SideSeparator(4, make.it.littleDarker),
      make.Div(
        make.it.leftAlign,
        make.Div(make.it.flexRow, make.style.gap(6),
          make.with.style({alignItems: "flex-end"}),
          picButton(pic, popup, styles),
          make.Paragraph(t1)
        ),
        make.Separator(4),
        make.Paragraph(t2)
      )
    )
  }

  function sideParagraphWithMargin(text, ...mods) {
    return make.Div(...mods,
      make.it.marginOnHover,
      make.it.flexRow,
      make.style.gap(6),
      make.SideSeparator(4, make.it.littleDarker),
      make.Div(
        make.it.flexColumn, make.style.gap(6),
        make.Paragraph(text)
      ),
    )
  }

  function manualCloseText() {
    return picButton("close", "Закрыть", make.it.act.negative,
      () => make.other.closeCurrentNotice(),
    )
  }

  function manualNotice() {
    make.Notice([1000, Infinity, 1000, "manual"],
      make.Div(
        make.style.width("100%"),
        make.style.height("100%"),
        make.it.contented,
        make.color.lblue,
        make.Div(
          make.it.contented,
          make.style.minWidth("50vw"),
          make.style.maxWidth("60vw"),
          make.style.height("80vh"),
          ...manualHeader()
        )
      )
    )
  }

  function inputFull() {
    let acc;
    let out = make.Div(make.it.marginOnHover)
    let inp
    inp = make.Input(
      make.with.attr({placeholder: "Поле ввода"}),
      make.on.input((e) => out.element.classList.add("make-mark-changed")),
      make.on.inputTimeOut(3000, () => {
        out.element.classList.remove("make-mark-changed")
      }),
      make.Annotation(1500, 
        make.Div(
          make.it.popup,
          make.Paragraph("Нажмите на поле ввода для редактирования"),
          make.Paragraph("Если элемент подсвечен, то он сохранится через некоторое время"),
          make.Paragraph("Если вы перейдёте на другой элемент, то этот так же сохранится автоматически"),
        )
      )
    )

    acc = make.Div(
      make.with.css("make-mark-filtered"),
      make.it.flexRow,
      make.style.gap(6),
      inp,
      picButton("save", "Сохранить", make.it.act.positive),
      picButton("verify", "Подтвердить", make.it.act.positive),
      picButton("hide", "Скрыть", make.it.act.alternative,
      () => acc.element.classList.toggle("make-mark-deactivated")),
      picButton("share", "Поделиться", make.it.act.neutral),
      picButton("trash", "Удалить", make.it.act.negative),
      picButton("close", "Закрыть", make.it.act.negative),
    )
    out.addChild(acc)
    return out
  }

  return make.Div(
    make.Separator(6),
    make.Button(
      make.color.lblue,
      make.it.action,
      make.it.act.neutral,
      make.with.text("Руководство"),
      make.on.click(() => {
        manualNotice()
      })
    )
  )
}