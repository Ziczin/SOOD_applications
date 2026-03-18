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
  const actionNotice = await imp(`${window.prefab_url}/action_notice.js`)
  const popup = await imp(`${window.prefab_url}/popup.js`)
  const picButton = await imp(`${window.prefab_url}/pic_button.js`, popup, window.media_url);

  const csrfObj = await make.Query('/api/csrf-token').get()
  const qBase = make.Query("/api")
                    .via({"X-CSRFToken": csrfObj.csrfToken})
                    .on({405: () => make.Notice([500, 1500, 500],
                      make.Div(
                        makeIt.content,
                        makeIt.flexColumn,
                        Style.gap(6),
                        make.color.red,
                        Paragraph("Ошибка создания! Попробуйте снова")
                      )
                    )})
                    .view();
  const qCurrentUser = qBase.at("me").view();
  const me = await qCurrentUser.get()

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
    backButton("Наборы символов", '/applications/charsets-manager/'),
    backButton("Шаблоны полей", '/applications/fields-manager/')
  )
  document.getElementById("left-btns").appendChild(leftBtns.build());

  function enumElem({id, value, ph, enabled=true, container, visible, makeQuery}) {
    let acc;
    let out = make.Div(makeIt.marginOnHover)
    out.id = id
    let inp
    inp = make.Input(
     With.attr({
        value: value,
        placeholder: ph ? ph : value ? value : "Пустой элемент"
      }),
      make.on.input((e) =>
        out.element.classList.add("make-mark-changed")
      ),
      make.on.inputTimeOut(3000, () => {
        out.element.classList.remove("make-mark-changed")
        makeQuery.at(out.id).with({value: inp.element.value || ''}).patch()
        paragraphNotice("Сохранено!", make.color.lgreen)
      }),
      ...make.if(!enabled,
        Style.padding(6),
       With.attrs("disabled"),
        make.Annotation(1500, 
          make.Div(
            makeIt.popup,
            Paragraph("Вы не можете редактировать этот элемент"),
          )
        ),
      ),
      ...make.if(enabled,
        make.Annotation(1500, 
          make.Div(
            makeIt.popup,
            Paragraph("Нажмите на поле ввода для редактирования"),
            Paragraph("Если элемент подсвечен, то он сохранится через некоторое время"),
            Paragraph("Если вы перейдёте на другой элемент, то этот так же сохранится автоматически"),
          )
        )
      )
    )
    acc = make.Div(
     With.css("make-mark-filtered"),
      ...make.if(!visible,
       With.css("make-mark-deactivated")
      ),
      makeIt.flexRow,
      Style.gap(6),
      inp,
      ...make.if(enabled,
        picButton("hide", "Скрыть элемент от пользователя", makeIt.act.alternative,
        () => {
          acc.element.classList.toggle("make-mark-deactivated")
          makeQuery.at(out.id).with({visible: !visible}).patch()
          paragraphNotice("Видимость изменена!", make.color.yellow)
        }),
        picButton("trash", "Удалить элемент", makeIt.act.negative,
          () => actionNotice({
            confirmText: "Удалить", cancelText: "Отмена",
            question: `Удалить ${inp.element.value || "*пустой элемент*"}?`,
            action: () => {
              container.removeChild(out)
              makeQuery.at(out.id).with({available: false}).patch()
              paragraphNotice("Удалено!", make.color.red)
            }
          })
        ),
      )
    )
    out.addChild(acc)
    return out
  }

  function createCollector(items, enabled=true) {
    let collector = make.Scrollbox(
      makeIt.flexColumn,
      Style.gap(6)
    )
    collector.addModifiers(
      ...items.map((item) => 
        enumElem({
          id: item.id,
          value: item.value,
          visible: item.visible,
          enabled: enabled,
          container: collector,
          makeQuery: qEnum,
        })
      )
    )
    return collector
  }
  
  function enumElemButtonAdd(enumCollector, qEnum, tag) {
    return make.Button(
      makeIt.action,
      makeIt.act.neutral,
     With.text("Добавить элемент"),
     With.style({flex: 1}),
      make.on.click(
        async () => {
          const newEnum = await qEnum.with({
            enum_tag: tag.id
          }).post()
          if (newEnum && !newEnum['detail']) {
            document.activeElement.blur()
            let enEl = enumElem({
              container: enumCollector,
              makeQuery: qEnum,
              ...newEnum
            })
            enumCollector.addChild(enEl)
            paragraphNotice("Создано!", make.color.lblue)
            enEl.element.querySelector("input").focus()
          }
        }
      )
    )
  }

  function centerComponent(qEnumm, items, tag, me) {
    return make.Div(
      Style.height('100%'),
      makeIt.flexColumn,
      Style.gap(6),
      enumCollector = createCollector(items, tag.department === me.department.id),
      ...make.if(
        tag.department === me.department.id,
        make.Div(
         With.style({flex: 0}),
          makeIt.flexRow,
          Style.gap(6),
          enumElemButtonAdd(enumCollector, qEnum, tag)
        ),
      ),
    ).build()
  }

  function enumTagPopup(owner_dep) {
    if (owner_dep) {
      return popup(
        "Это перечисление вашего отдела",
        "Кликните по полю ввода чтобы загрузить элементы этого перечисления")
    } else {
      return popup(
        "Другой отдел поделился этим перечислением",
        "Вы не можете его редактировать. Кликните для просмотра"
      )
    }
  }

  async function fillCenter(qEnum, qEnumTag, tag, me) {
    clearCenter().appendChild(
      centerComponent(qEnum, (await qEnumTag.at(tag.id).at("items").get()), tag, me)
    )
  }

    function clearCenter(doClear=true) {
      if (doClear) {
        let center = document.getElementById("center-content")
        center.innerHTML = ""
        return center
      }
    }

  function setUniqueClass(element, className = 'active') {
    document.querySelectorAll(`.${className}`).forEach(el => {
        el.classList.remove(className);
    });
    
    element.classList.add(className);
  }

  let selectedEnumTagId
  function enumTagElem(qEnum, qEnumTag, acc, me, tag) {
    let out
    let inp
    let shareBtn
    inp = make.Input(
      ...make.if(tag.department !== me.department.id,
       With.attrs('readonly'),
       With.css('fake-disabled')
      ),
      make.on.input((e) =>
        out.element.classList.add("make-mark-changed")
      ),
      make.on.inputTimeOut(3000, () => {
        out.element.classList.remove("make-mark-changed")
        qEnumTag.at(tag.id).with({name: inp.element.value || ''}).patch()
        paragraphNotice("Сохранено!", make.color.lgreen)
      }),
      enumTagPopup(tag.department === me.department.id),
     With.attr({ value: tag.name, placeholder: tag.name ? tag.name : 'Пустая группа'}),
      Style.padding(6),
      make.on.click(async () => {
        if (!inp?.element?.classList?.contains('make-mark-selected-group')){
          selectedEnumTagId = tag.id
          setUniqueClass(inp.element, 'make-mark-selected-group')
          await fillCenter(qEnum, qEnumTag, tag, me)
        }
      })
    )
    out = make.Div(
      ...make.if(!tag.visible,
       With.css("make-mark-deactivated")
      ),
      makeIt.flexRow, Style.gap(6), makeIt.marginOnHover, inp,
      ...make.if(!tag.shared || tag.department === me.department.id,
        picButton("hide", "Скрыть из вариантов при создании форм", makeIt.act.alternative,
        () => {
          out.element.classList.toggle("make-mark-deactivated")
          qEnumTag.at(tag.id).with({visible: !tag.visible}).patch()
          paragraphNotice("Видимость изменена!", make.color.yellow)
        }),
        ...make.if(!tag.shared,
          shareBtn = picButton("share", "Поделиться перечислением с другим отделом", makeIt.act.neutral,
          () => {
            actionNotice({
              confirmText: "Поделиться", cancelText: "Отмена",
              question: [
                Paragraph(`Поделиться ${inp.element.value || "*пустая группа*"} с другими отделами?`),
                Paragraph(`Это действие невозможно будет отменить`, makeIt.textBold),
              ],
              action: ()=>{
                out.removeChild(shareBtn),
                qEnumTag.at(tag.id).with({shared: !tag.shared}).patch()
                paragraphNotice("Видимость изменена!", make.color.yellow)
              }
            })
          })
        ),
        picButton("trash", "Удалить группу", makeIt.act.negative,
        () => {
          actionNotice({
            confirmText: "Удалить", cancelText: "Отмена",
            question: [
              Paragraph(`Удалить ${inp.element.value || "*пустая группа*"}?`),
              Paragraph(`Элементы перечисления так же будут удалены`, makeIt.textBold),

            ],
            action: ()=>{
              acc.removeChild(out)
              qEnumTag.at(tag.id).with({available: false}).patch()
              paragraphNotice("Удалено!", make.color.red),
              clearCenter(tag.id === selectedEnumTagId)
            }
          })
        })
      )
    )
    return out
  }


  async function leftContent(me, qEnumTag, qEnum) {
    let acc;

    let res = make.Div(
      makeIt.flexColumn,
      Style.gap(10),
      Style.height("100%"),
      make.h1(me.department.label),
      acc = make.Scrollbox(
        makeIt.flexColumn,
        Style.gap(6),
      )
    )
    acc.addModifiers(
      ...(await qEnumTag.get()).map((tag) =>
        enumTagElem(qEnum, qEnumTag, acc, me, tag)
      )
    )
    res.addModifiers(
      enumTagElemButtonAdd(me, acc, qEnumTag, qEnum)
    )
    return res
  }

  function enumTagElemButtonAdd(me, acc, qEnumTag, qEnum) {
    return make.Button(
      makeIt.action,
      makeIt.act.neutral,
      Style.maxHeight("fit-content"),
     With.text("Добавить группу"),
      make.on.click(
        async () => {
          document.activeElement?.blur()
          let tag = enumTagElem(qEnum, qEnumTag, acc, me,
            (await qEnumTag.with({
              department: me.department.id
            }).post()))
          if (tag) {
            acc.addChild(tag)
            paragraphNotice("Создано!", make.color.lblue)
            tag.element.querySelector("input").focus()
          }
        }
      )
    )
  }

  
  const qEnum = qBase.at("enums").view()
  const qEnumTag = qBase.at("enum-tags").view()
  
  let enumCollector = make.Scrollbox();


  document.getElementById("left-content").appendChild(
    (await leftContent(me, qEnumTag, qEnum)).build())

}