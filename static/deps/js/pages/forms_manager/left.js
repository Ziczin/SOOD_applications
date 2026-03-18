export default async () =>
{
  await import(`${window.make_url}/make.js`);

  const Style = make.style
  const makeIt = make.it
  const Paragraph = make.Paragraph
  const With = make.with
  const Gap = Style.gap

  const imp = (await import(`${window.prefab_url}/import.js`)).default(make)
  const paragraphNotice = await imp(`${window.prefab_url}/paragraph_notice.js`)
  const backButton = await imp(`${window.prefab_url}/exit_button.js`)
  const actionNotice = await imp(`${window.prefab_url}/action_notice.js`)
  const popup = await imp(`${window.prefab_url}/popup.js`)
  const picButton = await imp(`${window.prefab_url}/pic_button.js`, popup, window.media_url);

  const csrfObj = await make.Query('/api/csrf-token').get()
  const qBase = make.Query('/api').via({"X-CSRFToken": csrfObj.csrfToken}).view();

  const basicManual = await imp(`${window.manual_url}/basic_manual.js`, popup, picButton);
  const mainManual = await imp(`${window.manual_url}/main_manual.js`, ["user", "moderator", "admin"], qBase)
  
  document.getElementById('manual-button').appendChild(basicManual(mainManual).build())

  const leftBtns = make.Card(
    Style.rounded(12),
    Style.padding(6),
    makeIt.content
  )
  .header(makeIt.marginOnHover, make.h3("Перейти", makeIt.subtitleText))
  .content(
    makeIt.flexColumn,
    Gap(6),
    make.Separator(),
    backButton(),
    backButton("Перечисления", '/applications/enums-manager/'),
    backButton("Наборы символов", '/applications/charsets-manager/'),
    backButton("Шаблоны полей", '/applications/fields-manager/')
  )
  document.getElementById("left-btns").appendChild(leftBtns.build());



  const qForm = qBase.at('forms').view()
  const qField = qBase.at('fields').view()
  const qFormField = qBase.at('form-fields').view()
  const qFormFieldSwap = qFormField.at('swap').view()
  async function qFormFieldSwapById(fr, to) {
    await qFormFieldSwap.with({a: fr, b: to}).patch()
  }
  const fieldTypes = await qBase.at('field-types').get()
  const fields = {}
  for (const ft of fieldTypes) {
    let res = await qField.where({type: ft.id}).get()
    fields[ft.id] = res
  }

  const me = await qBase.at('me').get()
  const forms = await qForm.where({department: me.department.id}).get()
  
  let selectedFormId
  function formElem(acc, form) {
    let out
    let inp
    let shareBtn
    inp = make.Input(
      make.on.input((e) =>
        out.element.classList.add("make-mark-changed")
      ),
      make.on.inputTimeOut(3000, () => {
        out.element.classList.remove("make-mark-changed")
        qForm.at(form.id).with({label: inp.element.value || ''}).patch()
        paragraphNotice("Сохранено!", make.color.lgreen)
      }),
      popup("Нажмите на поле ввода, чтобы редактировать имя формы"),
      With.attr({ value: form.label, placeholder: form.label ? form.label : 'Новая форма'}),
      Style.padding(6),
      make.on.click(async () => {
        if (!inp?.element?.classList?.contains('make-mark-selected-group')){
          selectedFormId = form.id
          setUniqueClass(inp.element, 'make-mark-selected-group')
          await fillCenter(form)
        }
      })
    )
    out = make.Div(
      ...make.if(!form.visible,
        With.css("make-mark-deactivated")
      ),
      makeIt.flexRow, Gap(6), makeIt.marginOnHover, inp,
      picButton("hide", "Сделать форму невидимой для пользователей", makeIt.act.alternative,
      () => {
        out.element.classList.toggle("make-mark-deactivated")
        qForm.at(form.id).with({visible: !form.visible}).patch()
        paragraphNotice("Видимость изменена!", make.color.yellow)
      }),
      picButton("trash", "Удалить форму", makeIt.act.negative,
      () => {
        actionNotice({
          confirmText: "Удалить", cancelText: "Отмена",
          question: [
            Paragraph(`Удалить ${inp.element.value || "*Новая форма*"}?`),
            Paragraph(`Это действие невозможно отменить`, makeIt.textBold),

          ],
          action: ()=>{
            acc.removeChild(out)
            qForm.at(form.id).with({available: false}).patch()
            paragraphNotice("Удалено!", make.color.red),
            clearCenter(form.id === selectedFormId)
          }
        })
      })
    )
    return out
  }

  function setUniqueClass(element, className = 'active') {
    document.querySelectorAll(`.${className}`).forEach(el => {
        el.classList.remove(className);
    });
    element.classList.add(className);
  }

  function formAddButton(acc) {
    return make.Button(
      makeIt.action,
      makeIt.act.neutral,
      With.text("Добавить форму"),
      Style.maxHeight("fit-content"),
      make.on.click(
        async () => {
          let newForm = await qForm.with({
            department: me.department.id
          }).post()
          let form = formElem(acc, newForm)
          acc.addChild(form)
          paragraphNotice("Создано!", make.color.lblue)
          form.element.querySelector("input").focus()
          await fillCenter(newForm)
        }
      )
    )
  }
  
  function clearCenter(doClear=true) {
    if (doClear) {
      let center = document.getElementById("center-content")
      center.innerHTML = ""
      return center
    }
  }

  function leftContent() {
    let acc
    let ret = make.Div(
      makeIt.flexColumn,
      Style.height("100%"),
      Gap(10),
      make.h1("Формы"),
      acc = make.Scrollbox(
        makeIt.flexRow,
        Gap(6),
      ),
      formAddButton(acc)
    )
    
    acc.addModifiers(
      ...forms.map((form) =>
        formElem(acc, form)
      )
    )
    return ret
  }

  function formFieldElem(acc, formField) {
    let field = formField.field
    let ret = make.Div()
    ret.id = formField.id
    let prev = null
    if (acc.children.length !== 0) {
      prev = acc.children.at(-1)
      prev.nextFormFieldElem = ret
    }
    ret.prevFormFieldElem = prev
    ret.nextFormFieldElem = null

    let addit = ""
    if (field.tag) {
      addit = ` "${field.tag.label}"`
    }
    if (field.charset) {
      addit = ` "${field.charset.humanized_preview}"`
    }
    ret.addModifiers(
      makeIt.marginOnHover,
      make.Div(
        Style.padding(2),
        Style.rounded(12),
        With.css('recolor-on-hover'),
        makeIt.flexRow,
        With.style({
          justifyContent: "space-between", alignItems: "center",
          paddingLeft: "8px", paddingRight: "8px",
        }),
        make.Div(
          make.Div(
            makeIt.flexColumn,
            Paragraph(field.label),
            Paragraph(
			  field.type + addit, makeIt.subtitleText,
				...make.if(field.placeholder,
				  popup(["Плейсхолдер:", `"${field.placeholder}"`])
			  )
			)
          )
        ),
        make.Div(
          make.Div(
            makeIt.flexRow,
            Gap(6),
            picButton(
              "up", "Поднять поле на форме", makeIt.act.neutral,
              () => {
                if (ret.prevFormFieldElem !== null) {
                  let prev = ret.prevFormFieldElem
                  let prevPrev = prev.prevFormFieldElem
                  let currNext = ret.nextFormFieldElem
                  if (currNext) currNext.prevFormFieldElem = prev
                  prev.nextFormFieldElem = currNext
                  prev.prevFormFieldElem = ret
                  ret.nextFormFieldElem = prev
                  ret.prevFormFieldElem = prevPrev
                  if (prevPrev) prevPrev.nextFormFieldElem = ret
                  prev.swap(ret)
                  qFormFieldSwapById(ret.id, prev.id)
                }
                else {
                  paragraphNotice("Выше ничего нет", make.color.yellow)
                }
              }
            ),
            picButton(
              "trash", "Удалить", makeIt.act.negative,
              () => {
                actionNotice({
                  confirmText: "Удалить", cancelText: "Отмена",
                  question: [
                    Paragraph(`Вы уверены что хотите удалить это поле из формы?`),
                  ],
                  action: async () => {
                    qFormField.at(ret.id).with({available: false}).view().patch()
                    let next = ret.nextFormFieldElem
                    let prev = ret.prevFormFieldElem
                    if (prev) prev.nextFormFieldElem = next
                    if (next) next.prevFormFieldElem = prev
                    acc.removeChild(ret)
                  }
                })
              }
            ),
            picButton(
              "down", "Опустить поле на форме", makeIt.act.neutral,
              () => {
                if (ret.nextFormFieldElem !== null) {
                  let next = ret.nextFormFieldElem
                  let nextNext = next.nextFormFieldElem
                  let currPrev = ret.prevFormFieldElem
                  next.nextFormFieldElem = ret
                  next.prevFormFieldElem = currPrev
                  if (currPrev) currPrev.nextFormFieldElem = next
                  if (nextNext) nextNext.prevFormFieldElem = ret
                  ret.nextFormFieldElem = nextNext
                  ret.prevFormFieldElem = next
                  ret.swap(next)
                  qFormFieldSwapById(ret.id, next.id)
                }
                else {
                  paragraphNotice("Ниже ничего нет", make.color.yellow)
                }
              }
            ),
            (() => {
              const wrapper = make.Checkbox(
                popup(200, "Является ли поле обязательным для заполнения"),
                ...make.callif(formField.required,
                  () => With.attrs('checked')
                ),
                make.on.change((e) => {
                  qFormField.at(formField.id).with({required: wrapper.element.checked}).view().patch()
                })
              )
              return wrapper
            })()
          ),
        ),
      )
    )
    return ret
  }

  async function fillCenter(form) {
    clearCenter().appendChild(
      centerComponent(
        (await qFormField.where({form: form.id}).get())
      )
    )
  }
  
  let formFieldLinkedList
  function centerElem(items) {
    formFieldLinkedList = make.Scrollbox(
      makeIt.flexColumn,
      Gap(6)
    )
    for (const item of items) {
      formFieldLinkedList.addChild(formFieldElem(formFieldLinkedList, item))
    }
    return formFieldLinkedList
  }

  function centerComponent(formFields) {
    let acc
    return make.Div(
      make.h1("Поля формы", With.style({marginLeft: "6px", marginTop: "6px"})),
      Style.height('100%'),
      makeIt.flexColumn,
      Gap(6),
      acc = centerElem(formFields),
    ).build()
  }

  function rightContent() {
    return make.Div(
      Style.height('100%'),
      makeIt.flexColumn,
      Gap(6),
      make.h1("Доступные шаблоны"),
      make.Scrollbox(
        makeIt.flexColumn,
        Gap(6),
        ...fieldTypes.map((ft) => 
          make.Card(
            Style.rounded(12),
            Style.padding(4),
            makeIt.littleDarker,
          )
          .header(
            Style.rounded(12),
            Style.padding(4),
            With.css('recolor-on-hover'),
            Paragraph(ft.label),
          )
          .content(
            make.Div(
              Style.padding(8),
              Style.rounded(12),
              make.Div(
                makeIt.flexColumn,
                Gap(6),
                ...make.if(fields[ft.id].length,
                  ...fields[ft.id].map((f)=>
                    make.Div(
                      With.style({alignItems: "center"}),
                      makeIt.marginOnHover,
                      makeIt.flexRow,
                      Gap(6),
                      picButton("plus", "Добавить шаблон на форму", makeIt.act.positive, async () => {
                        formFieldLinkedList.addChild(
                          formFieldElem(
                            formFieldLinkedList, (await qFormField.with({form: selectedFormId, field_id: f.id}).post())
                          )
                        )
                      }),
                      Paragraph(f.label)
                    )
                  )
                ),
                ...make.if(!fields[ft.id].length,
                  Paragraph("Не найдено шаблонов под данному типу")
                )
              )
            )
          )
        )
      )
    )
  }

  document.getElementById("right-content").appendChild(rightContent().build())
  document.getElementById('center-container').style.padding = '6px';
  document.getElementById("left-content").appendChild(leftContent().build())

}