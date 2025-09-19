export default (make, popup, picButton, enumElem) =>
function enumManagerManual() {
  function manualContent() {
    let styleTab = [make.style.padding(4), make.it.littleDarker]
    return [
      make.Div(
        make.it.flexRow, make.style.gap(6), make.style.maxHeight("10%"),
        make.h1("Руководство"),
        manualCloseText(),
      ),
      make.Separator(6),
      make.Tabs(
        make.style.width("100%"),
        make.style.height("100%"),
      )
      .menu(make.it.littleDarker, make.style.gap(6), make.style.rounded(12), make.style.padding(4))
      .content(make.style.maxHeight("auto"))
      .tab()
      .header(...styleTab, make.Paragraph("Главная"))
      .content(
        make.style.maxHeight("100%"),
        make.it.flexColumn, make.style.gap(6),
        make.Paragraph("• Это руководство кратко описывает алгоритм работы с данной страницей"),
        make.Paragraph("• Выше, находятся вкладки, на которых расписан основной функционал"),
        make.Paragraph("• Руководство предназначено для тех, кто в отделе был назначен администратором"),
        make.Paragraph("• Пишите в отдел программирования если остался вопрос, на который в данном руководстве нет ответа"),
        make.Separator(0),
        make.Paragraph(`Можете перейти на вкладку "Подсказки"`),
        sideParagraphWithMargin("Если вас не устраивает размер текста, то вы можете изменить его сами " +
          "используя страндартные инструменты браузера: CTRL + \"+\" для увеличения размера элементов, " +
          "CTRL + \"-\" для уменьшения размера элементов", make.it.subtitleText),
      )
      .tab()
      .header(...styleTab, make.Paragraph("Подсказки"))
      .content(
        make.it.flexColumn, make.style.gap(6),
        make.Paragraph("• Большая часть элементов при наведении выведет вам подсказку через 1.5 секунды"),
        make.Paragraph("Наведитесь на эту строку и подождите несколько секунд", make.with.style({textDecoration: "underline"}),
        popup([
          "Так будет выглядить подсказка",
          "Зачастую, в подсказках будут проянены некоторые моменты",
          "которые могут показаться неочевидными на первый взгляд"
        ]),
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
            popup(800, [
              "Это подсказка на поле ввода",
              "подсказки могут находиться на элементах, даже если те отключены"
            ])
          ),
          make.Button(make.it.redir, make.with.text("это кнопка"),
            popup(800, "Это подсказка на кнопке"), make.with.style({whiteSpace: "nowrap"}),
            make.on.click((e) => e.target.textContent = "Тут нет ничего интересного")
          ),
          make.Div(
            make.it.flexRow,
            make.style.gap(6),
            make.style.minWidth("24%"),
            picButton("save", "Это подсказка на кнопке сохранения"),
            picButton("hide", "Подсказка на кнопке сохранения"),
            picButton("share", `Это кнопка "Поделиться"`),
            picButton("trash", `Это "Удалить"`),
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
        make.Paragraph("• Например:"),
        enumElem({id: 0, value: "Демонстрационное поле", visible: true, test: true}),
        make.Separator(0),
        make.Paragraph("• Кнопки имеют смысл в контексте того, где они находятся, наведитесь на них чтобы увидеть описание их действий"),
        make.Separator(0),
        make.Paragraph("• Разберём что из себя представляют кнопки на данной странице:"),
        make.Div(
          make.it.flexColumn, make.style.gap(6),
          manualFunctionalButtonElement(
            "save", [`"Дискета"`, "Сохранить"], make.it.act.positive,
            "Кнопки с изображением дискеты обычно сохраняют изменения в базу данных",
            "На данной странице такие кнопки фиксируют в базе новое значение из поля ввода",
          ),
          manualFunctionalButtonElement(
            "hide", [`"Глаз"`, "Скрыть/показать"], make.it.act.alternative,
            "Кнопки с изображением глаза обычно скрывают или раскрывают данные",
            "На данной странице такие кнопки фиксируют в базе видимость элемента для других страниц",
          ),
          manualFunctionalButtonElement(
            "share", [`"Граф"`, "Поделиться"], make.it.act.neutral,
            "Кнопки с изображением графа обычно означают что этим элементом можно поделиться",
            "На данной странице такие кнопки дают разрешение другим " +
            "отделам просматривать и использовать перечисление, которым вы делитесь",
          ),
          manualFunctionalButtonElement(
            "trash", [`"Корзина"`, "Удалить"], make.it.act.negative,
            "Кнопки с изображением корзины обычно удаляют запись из базы данных",
            "На данной странице такие кнопки делают запись невидимой для любого пользователя, " +
            "кроме администратора, но она всё ещё будет видна в тех заявках и формах, где уже была применена ранее",
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
          enumElem({id: 0, value: `Поле №${i}`, visible: true, test: true}),
        ),
        make.Paragraph("Нажмите на первое поле ввода и нажимайте TAB, " +
          "пока не окажитесь на нужной кнопке, после чего нажмите ПРОБЕЛ", make.it.subtitleText),
      )
    ]
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
    return make.Paragraph(
      "Нажмите на эту строку, чтобы скрыть руководство",
      make.it.subtitleText,
      make.on.click(() => make.other.closeCurrentNotice()),
      make.with.style({alignSelf: "flex-end", fontSize: "16px"})
    )
  }

  function manual() {
    make.UniqueNotice("manual", 1000, Infinity, 1000,
      make.Div(
        make.style.width("100%"),
        make.style.height("100%"),
        make.it.content,
        make.color.lblue,
        make.Div(
          make.it.content,
          make.style.minWidth("50vw"),
          make.style.maxWidth("60vw"),
          make.style.height("80vh"),
          ...manualContent()
        )
      )
    )
  }

  return make.Div(
    make.Separator(6),
    make.Button(
      make.color.lblue,
      make.it.action,
      make.it.act.neutral,
      make.with.text("Руководство"),
      make.on.click(() => {
        manual()
      })
    )
  )
}