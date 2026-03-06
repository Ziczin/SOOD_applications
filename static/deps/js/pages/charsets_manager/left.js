
export default async () =>
{
  await import(`${window.make_url}/make.js`);
  const imp = (await import(`${window.prefab_url}/import.js`)).default(make)

  const paragraphNoticePromise = imp(`${window.prefab_url}/paragraph_notice.js`)
  const actionNoticePromise = imp(`${window.prefab_url}/action_notice.js`)
  const backButtonPromise = imp(`${window.prefab_url}/exit_button.js`)
  const popupPromise = imp(`${window.prefab_url}/popup.js`)

  const [paragraphNotice, backButton, actionNotice, popup,] = await Promise.all(
    [paragraphNoticePromise, backButtonPromise, actionNoticePromise, popupPromise]
  )
  const picButton = await imp(`${window.prefab_url}/pic_button.js`, popup, window.media_url);

  const csrfObj = await make.Query('/api/csrf-token').get()
  const qBase = make.Query("/api").via({"X-CSRFToken": csrfObj.csrfToken}).view();
  const me = await qBase.at("me").view().get()
  const qFieldCharSet = qBase.at('field-charsets').view()

  const basicManual = await imp(`${window.manual_url}/basic_manual.js`, popup, picButton)
  const mainManual = await imp(`${window.manual_url}/main_manual.js`, me.permissions, qBase)

  document.getElementById('manual-button').appendChild(basicManual(mainManual).build())

  const leftBtns = make.Card(
    make.style.rounded(12),
    make.style.padding(6),
    make.it.content
  )
  .header(make.it.marginOnHover, make.h3("Перейти", make.it.subtitleText))
  .content(
    make.it.flexColumn,
    make.style.gap(6),
    make.Separator(),
    backButton(),
    backButton("Формы", '/applications/forms-manager/'),
    backButton("Перечисления", '/applications/enums-manager/'),
    backButton("Шаблоны полей", '/applications/fields-manager/')
  )
  document.getElementById("left-btns").appendChild(leftBtns.build());


  const Row = (...args) => make.Div(make.it.flexRow, make.style.gap(6), ...args)
  const Column = (...args) => make.Div(make.it.flexColumn, make.style.gap(6), ...args)

  const initFieldCharSets = await qFieldCharSet.get()
  const center = document.getElementById("center-content")

  function Input(charset, value, label, queryparam, type="check") {
    return Row(
      make.it.marginOnHover,
      ...make.callif(type === 'check',
        () => make.Checkbox(
          ...make.callif(
            charset.department !== me.department.id,
            () => make.with.attrs("disabled")
          ),
          ...make.callif(value,
            () => make.with.attrs('checked')
          ),
          make.on.change((e) => {
            qFieldCharSet.at(charset.id).with({
              [queryparam]: e.target.checked
            }).view().patch()
            charset[queryparam] = e.target.checked
            paragraphNotice("Сохранено!", make.color.green)
          })
        ),
      ),
      make.Paragraph(label, make.with.style({alignSelf: "center", flex: '0 0 auto'})),
      ...make.callif(type !== 'check', () => make.style.padding(4)),
      ...make.callif(type !== 'check',
        () => make.Input(
          ...make.callif(
            charset.department !== me.department.id,
            () => make.with.attrs("disabled")
          ),
          ...make.callif(['min_length', 'max_length'].includes(queryparam),
            () => make.limit.charactersWhiteList("1234567890")
          ),
          make.with.attr({value: value ? value : ''}),
          make.on.input((e) => e.target.parentNode.classList.add("make-mark-changed")),
          make.on.inputTimeOut(3000, (e) => {
            qFieldCharSet.at(charset.id).with({
              [queryparam]: e.target.value
            }).view().patch()
            charset[queryparam] = e.target.value
            e.target.parentNode.classList.remove("make-mark-changed")
            paragraphNotice("Сохранено!", make.color.green)
          })
        ),
      ),
    )
  }

  function charSetDataDraw(charset) {
    center.innerHTML = ''
    center.appendChild(
      Column(
        Input(charset, charset.cyrillic_lower, "Кириллица строчные", "cyrillic_lower"),
        Input(charset, charset.cyrillic_upper, "Кириллица ЗАГЛАВНЫЕ", "cyrillic_upper"),
        Input(charset, charset.latin_lower, "Латиница строчные", "latin_lower"),
        Input(charset, charset.latin_upper, "Латиница ЗАГЛАВНЫЕ", "latin_upper"),
        Input(charset, charset.space, "Пробел", "space"),
        Input(charset, charset.digits, "Цифры", "digits"),
        Input(charset, charset.special, "Спец. символы", "special"),
        Input(charset, charset.included, "Включая символы", "included", 'inp'),
        Input(charset, charset.excluded, "Исключая символы", "excluded", 'inp'),
        Input(charset, charset.min_lenght, "Минимальная длинна строки", "min_length", 'inp'),
        Input(charset, charset.max_lenght, "Максимальная длинна строки", "max_length", 'inp')
      ).build()
    )
  }

  function charSetElem(charset) {
    let picBTNS
    const elem = Row(make.it.marginOnHover)
    elem.charset = charset
    elem.addModifiers(
      make.Input(
        make.with.attr({
          value: charset.label,
          placeholder: charset.label
        }),
        ...make.callif(
            charset.department !== me.department.id,
            () => [make.with.attrs("readonly"), make.with.css('fake-disabled')]
          ),
        make.on.click(() => {
          charSetDataDraw(charset)
        }),
        make.on.input((e) => e.target.parentNode.classList.add("make-mark-changed")),
        make.on.inputTimeOut(3000, (e) => {
          qFieldCharSet.at(charset.id).with({
            label: e.target.value
          }).view().patch()
          e.target.parentNode.classList.remove("make-mark-changed")
          paragraphNotice("Сохранено!", make.color.green)
        })
      ),
      ...make.callif(!charset.visible, () => make.with.css("make-mark-deactivated")),
      ...make.if(!charset.shared,
        picBTNS = Row(
          picButton("hide", "Скрыть из вариантов при создании форм", make.it.act.alternative,
            () => {
              elem.element.classList.toggle("make-mark-deactivated")
              qFieldCharSet.at(charset.id).with({visible: !charset.visible}).patch()
              charset.visible = !charset.visible
              paragraphNotice("Видимость изменена!", make.color.yellow)
            }
          ),
          picButton("share", "Поделиться набором с другим отделом", make.it.act.neutral,
            () => {
              actionNotice({
                confirmText: "Поделиться", cancelText: "Отмена",
                question: [
                  make.Paragraph(`Поделиться ${elem.element.value || "*пустой набор*"} с другими отделами?`),
                  make.Paragraph(`Это действие невозможно будет отменить`, make.it.textBold),
                ],
                action: ()=>{
                  qFieldCharSet.at(charset.id).with({shared: true}).patch()
                  picBTNS.parent.removeChild(picBTNS)
                  paragraphNotice("Видимость изменена!", make.color.yellow)
                }
              })
            }
          ),
          picButton("trash", "Удалить элемент", make.it.act.negative,
            () => actionNotice({
              confirmText: "Удалить", cancelText: "Отмена",
              question: `Удалить ${elem.element.value || "*пустой набор*"}?`,
              action: () => {
                qFieldCharSet.at(charset.id).with({available: false}).patch()
                elem.parent.removeChild(elem)
                center.innerHTML = ''
                paragraphNotice("Удалено!", make.color.red)
              }
            })
          ),
        )
      )
    )
    return elem
  }
  let scrollbox
  document.getElementById("left-content").appendChild(
    Column(
      make.style.height("100%"),
      scrollbox = make.Scrollbox(
        make.style.gap(6),
        ...initFieldCharSets.map((ifcs) => charSetElem(ifcs))
      ),
      make.Button(
        make.with.text("Добавить новый набор"),
        make.it.action,
        make.it.act.positive,
        make.on.click(async () => {
          const newCharset = await qFieldCharSet.with({
            department: me.department.id
          }).post()
          const newElem = charSetElem(newCharset)
          scrollbox.addChild(
            newElem
          )
          newElem.element.focus()
        })
      )
    ).build()
  )
}