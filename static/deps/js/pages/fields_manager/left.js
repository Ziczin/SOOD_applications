export default async () =>
{
  await import(`${window.make_url}/make.js`);

  const Style = make.style
  const makeIt = make.it
  const Paragraph = make.Paragraph
  const With = make.with

  const imp = (await import(`${window.prefab_url}/import.js`)).default(make)
  const paragraphNotice = await imp(`${window.prefab_url}/paragraph_notice.js`)
  const backButton = await imp(`${window.prefab_url}/exit_button.js`)
  const popup = await imp(`${window.prefab_url}/popup.js`)
  const picButton = await imp(`${window.prefab_url}/pic_button.js`, popup, window.media_url);

  const csrfObj = await make.Query('/api/csrf-token').get()
  const qBase = make.Query("/api")
                    .via({"X-CSRFToken": csrfObj.csrfToken})
                    .view();
  
  const me = await qBase.at("me").view().get()
  const basicManual = await imp(`${window.manual_url}/basic_manual.js`, popup, picButton);
  const mainManual = await imp(`${window.manual_url}/main_manual.js`, me.permissions, qBase)
  
  document.getElementById('manual-button').appendChild(basicManual(mainManual).build())

  const leftBtns = make.Card(
    Style.rounded(12),
    Style.padding(6),
    makeIt.content
  )
  .header(makeIt.marginOnHover, make.h3("Перейти", makeIt.subtitleText))
  .content(
    makeIt.flexColumn,
    Style.gap(6),
    make.Separator(),
    backButton(),
    backButton("Формы", '/applications/forms-manager/'),
    backButton("Перечисления", '/applications/enums-manager/'),
    backButton("Наборы символов", '/applications/charsets-manager/'),
  )
  document.getElementById("left-btns").appendChild(leftBtns.build());


  
  const mePromise = qBase.at("me").view().get()

  const qFields = qBase.at('fields').view()
  const qFieldTypes = qBase.at('field-types').view();

  const qEnumTags = qBase.at('enum-tags').view()
  const qEnumTagsHistory = qEnumTags.at('history').view()

  const qFieldCharsets = qBase.at('field-charsets').view()
  const qFieldCharsetsHistory = qFieldCharsets.at('history').view()

  const fieldTypesPromise = qFieldTypes.get()
  
  const enumTagsPromise = qEnumTags.get()
  const enumTagsHistoryPromise = qEnumTagsHistory.get()

  const fieldCharsetsPromise = qFieldCharsets.get()
  const fieldCharsetsHistoryPromise = qFieldCharsetsHistory.get()


  const center = document.getElementById('center-container')

  const Row = (...mods) => make.Div(makeIt.flexRow, Style.gap(6), ...mods)
  const Column = (...mods) => make.Div(makeIt.flexColumn, Style.gap(6), ...mods)

  function enumField(field, inpField) {
    const select = make.Select(
      popup("Доступные перечисления")
    )
    async function fillField() {
      const enumTags = await enumTagsPromise
      const enumTagsHistory = await enumTagsHistoryPromise
      const exists = enumTags.some(tag => field.tag && tag.id === field.tag.id)
      let found
      if (!exists) { found = enumTagsHistory.find(tag => field.tag && tag.id === field.tag.id) }
      select.addModifiers(
        make.OptionPlaceholder("--- выбрать перечисление ---"),
        ...make.callif(found, () => {
          inpField.addModifiers(With.attrs("disabled"))
          return [make.Option(found.name, found.id), With.attrs("disabled")]
        }),
        ...enumTags.map(tag => make.Option(tag.name, tag.id)),
        make.on.change((e) => {
          if (!found) {
            qFields.at(field.id).with({tag: e.target.value}).view().patch()
            paragraphNotice("Изменено!", make.color.green)
          }
        })
      )
    }
    function setSelected() {
      select.children.forEach((ch) => {
        if (field.tag && ch.element.value == field.tag.id) {
          select.element.value = ch.element.value
        }
      })
      select.onBuild.unsub(setSelected)
    }
    select.allowEvents()
    select.onBuild.sub(() => setSelected())
    fillField()
    return select
  }

  function charsetField(field, inpField, placeholderField) {
    const select = make.Select(
      popup("Доступные наборы символов")
    )
    async function fillField() {
      const charsets = await fieldCharsetsPromise
      const charsetsHistory = await fieldCharsetsHistoryPromise

      const exists = charsets.some(set => set.id === field.charset?.id)
      let found
      if (!exists) { found = charsetsHistory.find(set => set.id === field.charset?.id) }
      select.addModifiers(
        make.OptionPlaceholder("--- выбрать набор символов ---"),
        ...make.callif(found, () => {
          inpField.addModifiers(With.attrs("disabled"))
          placeholderField.addModifiers(With.attrs("disabled"))
          console.log("HERE")
          return [make.Option(found.label, found.id), With.attrs("disabled")]
        }),
        ...charsets.map(set => make.Option(set.label, set.id)),
        make.on.change((e) => {
          if (!found) {
            qFields.at(field.id).with({charset: e.target.value}).view().patch()
            paragraphNotice("Изменено!", make.color.green)
          }
        })
      )
    }
    function setSelected() {
      select.children.forEach((ch) => {
        if (ch.element.value == field.charset?.id) {
          select.element.value = ch.element.value
        }
      })
      select.onBuild.unsub(setSelected)
    }
    select.allowEvents()
    select.onBuild.sub(() => setSelected())
    fillField()
    return select
  }

  function labelField(field, row) {
    const input = make.TextArea(
      popup("Название поля на форме"),
      With.attr({
        placeholder: field.label || "Название"
      }),
      With.style({
        height: "fit-content",
        display: "flex",
        flexDirection: "row",
		resize: "vertical",
      }),
    )
    input.addModifiers(
      make.on.input(() => row.element.classList.add("make-mark-changed")),
      make.on.inputTimeOut(3000, () => {
        qFields.at(field.id).with({label: input.element.value}).view().patch()
        row.element.classList.remove("make-mark-changed")
        paragraphNotice("Изменено!", make.color.green)
      })
    )
	
	input.allowEvents()
	input.onBuild.once(() => input.element.value = field.label )
    return input
  }

  function placeholderField(field, row) {
    const input = make.TextArea(
      popup("Подсказка для поля на форме", "Будет показываться серым цветом и не влияет на значение"),
      With.attr({
        value: field.placeholder || '',
        placeholder: field.placeholder || "Плейсхолдер",
      }),
      With.style({
        height: "auto",
        display: "flex",
        flexDirection: "row",
		resize: "vertical",
      }),
    )
    input.addModifiers(
      make.on.input(() => row.element.classList.add("make-mark-changed")),
      make.on.inputTimeOut(3000, () => {
        qFields.at(field.id).with({placeholder: input.element.value}).view().patch()
        row.element.classList.remove("make-mark-changed")
        paragraphNotice("Изменено!", make.color.green)
      })
    )
	input.allowEvents()
	input.onBuild.once(() => input.element.value = field.placeholder)
    return input
  }

  function decimalsField(field, row) {
    function elemDecimalFields(isPositive, queryArgument, popupText, placeholderText) { 
      const input = make.Input(
        popup(200, popupText),
        With.attr({
          type: "number",
          value: field[queryArgument],
          placeholder: placeholderText
        }),
        ...make.callif(isPositive, () => With.attr({min: 0})),
      )
      input.addModifiers(
        make.on.input(() => row.element.classList.add("make-mark-changed")),
        make.on.inputTimeOut(3000, () => {
          qFields.at(field.id).with({[queryArgument]: input.element.value}).view().patch()
          row.element.classList.remove("make-mark-changed")
          paragraphNotice("Изменено!", make.color.green)
        })
      )
      return input
    }
    
    return make.Card(
      makeIt.littleDarker,
      Style.rounded(12),
      Style.padding(6)
    )
    .header(
      popup("Нажмите чтобы скрыть или показать дополнительные параметры"),
      Paragraph("Дополнительно")
    )
    .content(
      makeIt.flexColumn,
      Style.gap(6),
      make.Separator(),
      elemDecimalFields(true, "decimals", "Количество знаков после запятой", "Точность"),
      elemDecimalFields(false, "minimum", "Минимальное допустимое значение", "Минимум"),
      elemDecimalFields(false, "maximum", "Максимальное допустимое значение", "Максимум")
    )
  }

  const doPlaceholder = [
    "text", "textarea", "number", "charset"
  ]
  function fieldFactory(field, type) {
    const row = Row(
      makeIt.marginOnHover,
      With.style({flex: "0 0 auto"})
    )
    const inpField = labelField(field, row)
    let placeholderFieldElem = null
    if (doPlaceholder.includes(type)) {
      placeholderFieldElem = placeholderField(field, row)
    }
    row.addModifiers(
      inpField,
      ...make.if(placeholderFieldElem, placeholderFieldElem),
      ...make.callif(type === "enum", () => enumField(field, inpField)),
      ...make.callif(type === "charset", () => charsetField(field, inpField, placeholderFieldElem)),
      ...make.callif(type === "number", () => decimalsField(field, inpField)),
    )
    return row
  }

  async function fillCenter(fieldType) {
    center.innerHTML = ``
    const fields = await qFields.where({type: fieldType.id}).view().get()
    const me = await mePromise
    const scrollbox = make.Scrollbox(makeIt.flexColumn, Style.gap(6))
    center.appendChild(
      Column(
        scrollbox.addModifiers(
          ...fields.map(field => fieldFactory(field, fieldType.type))
        ),
        make.Button(
          With.text("Добавить новый шаблон"),
          makeIt.action,
          makeIt.act.neutral,
          make.on.click(async () => {
            const newField = await qFields.with({
              type: fieldType.id,
              department: me.department.id
            }).view().post()
            const newRow = fieldFactory(newField, fieldType.type)
            scrollbox.addChild(
              newRow
            )
            newRow.children[0].element.focus()
          })
        )
      ).build()
    )
  }

  document.addEventListener('keydown', function(e){
    if(e.key !== 'Enter') return;
    const active = document.activeElement;
    if(!active) return;
    if(active === document.body) return;
    active.click();
    active.blur();
  });
  
  const boldText = (txt) => Paragraph(txt, makeIt.textBold)

  const fieldTypes = await fieldTypesPromise
  document.getElementById('left-content').appendChild(
    Column(
      ...fieldTypes.map(fieldType => 
        make.Button(
          makeIt.action,
          makeIt.act.neutral,
          With.text(fieldType.label),
          make.on.click(() => fillCenter(fieldType)),
          popup(
            ...make.switch(fieldType.name,
              make.case("text", boldText("Это просто строковое поле"), "Пользователь может ввести всё, что угодно", "Например: название, адрес"),
              make.case("textarea", boldText("Это текстовое поле"), "Пользователь может ввести некоторый объёмный текст", "Например: описание проблемы"),
              make.case("number", boldText("Это числовое поле"), "Пользователь может ввести число с точностью до указанной", "Например: 123.45"),
              make.case("date", boldText("Это просто дата"), "Например: дата отсутствия"),
              make.case("time", boldText("Это просто время"), "Например: Часы работы"),
              make.case("datetime", boldText("Это время и дата вместе"), "Например: дата и время встречи, дата и время приёма"),
              make.case("month", boldText("Это только месяц"), "Например: Август"),
              make.case("week", boldText("Это только неделя"), "Например: 34 неделя для отпуска"),
              make.case(
                "checkbox",
                boldText("Это чек-поле"),
                "Такое поле имеет всего два значения и не может быть обязательным",
                "Например: Работаете ли вы на свежем воздухе"
              ),
              make.case(
                "enum",
                boldText("Это перечисление"),
                "Для этого поля выбирается группа перечеслений",
                "Пользователь сможет выбрать перечисление из указанной группы",
                'Например, для группы перечеслений "Отделы" могут быть предложены варианты:',
                "• Отдел программирования",
                "• Абдоминальное отделение №1",
                "• Бухгалтерия",
                "... и другие"
              ),
              make.case(
                "charset",
                boldText("Это ограниченный символьный набор"),
                "Для таких полей могут быть разрешены к использованию лишь некоторые символы",
                "Например, если для такого набора разрешены только кириллические символы:",
                "• Разрешено: Иван Иванович",
                "• Запрещено: Иван123 Иванович456",
                "• Запрещено: Ivan Ivanovich",
                "Данное поле не показывает ошибку, а просто запрещает ввод неподходящих символов"
              ),
              make.endcase("Это эндкейс. Если вы его видите - это косяк разработчика")
            )
          )
        )
      )
    ).build()
  )

}