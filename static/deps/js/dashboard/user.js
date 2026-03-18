export default (make) =>
function dashboardUser(qBase, deps, forms, paragraphNotice, popup, rebuildFoo, picButton) {
    const Style = make.style
    const Paragraph = make.Paragraph
    const With = make.with
    const makeIt = make.it
    const scrollbox = make.Scrollbox(
        makeIt.flexColumn,
        Style.gap(6),
    )
    const cards = Object.fromEntries(
      Object.entries(deps).map(([key, value]) =>
        [key, make.Card(
          makeIt.marginOnHover,
          With.style({border: "3px solid #ddd", backgroundColor: "#f5f5f5"}),
          Style.padding(6),
          Style.rounded(12),
        ).header(
          Paragraph(value),
          popup("Нажмите чтобы развернуть список форм данного отдела"),
          make.color.lgray,
          Style.margin(-8),
          Style.padding(6),
          Style.rounded(12),
          With.style({border: "3px solid #ddd"}),
        ).content(
          make.Separator(6),
          Style.height('100%'),
          make.Div(
            With.style({paddingTop: "8px"}),
            Style.rounded(12),
            makeIt.flexColumn,
            Style.gap(6),
          )
        )]
      )
    );
    forms.forEach(form => {
      cards[form.department].cardContent.children[1].addChild(
        make.Div(
          makeIt.marginOnHover,
          make.Button(
            makeIt.redir,
            With.text(form.label || "Безымянная форма"),
            With.style({color: "#333"}),
            makeIt.leftAlign,
            make.on.click(async () => formModal(form.id)),
            popup(400, "Нажмите, чтобы открыть окно заполнения формы")
          )
        )
      )
    });

    function formFieldElem(field, type) {
      const wrapper = make.Div(
        makeIt.marginOnHover,
        Style.rounded(12),
        Style.padding(12),
        ...make.callif(
          field.required && field.type !== 'checkbox',
          () => With.css("have-status-REJECTED")
        ),
        ...make.callif(!field.required || field.type === 'checkbox', () => make.color.lgray)
      )
      if (type !== "checkbox") {
        wrapper.addModifiers(
          makeIt.flexColumn,
          Style.gap(6),
          Paragraph(field.label),
          (() => {
            const map = {
              text: () => textFieldElem(field),
              textarea: () => textareaFieldElem(field),
              number: () => numberFieldElem(field),
              date: () => dateFieldElem("date"),
              time: () => dateFieldElem("time"),
              datetime: () => dateFieldElem("datetime-local"),
              month: () => dateFieldElem("month"),
              week: () => dateFieldElem("week"),
              charset: () => charsetFieldElem(field),
              enum: () => enumField(field)
            };

            const fieldComp = map[type]()
            fieldComp.addModifiers(
              With.attr({id: field.id}),
              ...make.callif(field.required && field.type !== 'checkbox',
                () => [
                  popup(100,
                    "Это поле обязательно для заполнения",
                  ),
                  make.on.inputTimeOut(100, (e) => {
                    if (e.target.value) {
                      wrapper.element.classList.remove("have-status-REJECTED")
                      wrapper.element.classList.add("have-status-COMPLETED")
                    }
                    else {
                      wrapper.element.classList.remove("have-status-COMPLETED")
                      wrapper.element.classList.add("have-status-REJECTED")
                    }
                  })
                ]
              )
            )
            fieldComp.build()
            fieldComp.element.makeDataRequired = field.required || false
            return fieldComp
          })()
        )
      }
      else {
        wrapper.addModifiers(
          makeIt.flexRow,
          Style.gap(6),
          make.Checkbox(With.attr({id: field.id})),
          Paragraph(field.label, With.style({alignSelf: "center"})),
        )
      }
      return wrapper
    }

    function dateFieldElem(type) {
      return make.Input(
        With.attr({type: type})
      )
    }

    function textFieldElem(field) {
      return make.Input(
        With.attr({placeholder: field.placeholder || ''})
      )
    }

    function textareaFieldElem(field) {
      return make.TextArea(
        With.attr({
			placeholder: field.placeholder || ''
		}),
		With.style({
			resize: "vertical"
		})
      )
    }

    function numberFieldElem(field) {
      return make.Input(
        With.attr({type: "number"}),
        ...make.callif(field.decimals,
          () => make.limit.decimalPrecision(field.decimals)
        ),
        ...make.callif(field.minimum,
          () => With.attr({min: field.minimum})
        ),
        ...make.callif(field.maximum,
          () => With.attr({max: field.maximum})
        ),

      )
    }

    function charsetFieldElem(field) {
      return make.Input(
        With.attr({placeholder: field.placeholder || ''}),
        make.limit.charactersWhiteList(field.charset.preview),
        popup(2000, "Это ограниченное поле, доступные символы:",
          field.charset.humanized_preview
        ),
        ...make.callif(field.charset.min_length,
          () => With.attr({minlength: field.charset.min_length})
        ),  
        ...make.callif(field.charset.max_length,
          () => With.attr({maxlength: field.charset.max_length})
        )
      )
    }

    function enumField(field) {
      return make.Select(
        make.OptionPlaceholder(`--- выберите элемент--- `),
        ...field.enums.map(enu => make.Option(enu.value, enu.id))
      );
    }

    async function formModal(formId) {
      let data = await qBase.at('forms').at(formId).at('data').view().get()
      let collector = make.Collector()
      let popupCanSend
      let popupCantSend
      collector.allowEvents()
      collector.onAllRequiredFieldsFilled.sub(() => {
        if (collector.btn.element) {
          collector.btn.element.disabled = false
          if (popupCantSend) collector.btn.removeChild(popupCantSend)
          collector.btn.addChild(
            popupCanSend = popup(100, "Нажмите, чтобы отправить заявку")
          )
          collector.btn.element.classList.remove('make-btn-action-negative')
          collector.btn.element.classList.add('make-btn-action-positive')
        }
      })
      collector.onRequiredFieldMissing.sub(() => {
        if (collector.btn.element) {
          collector.btn.element.disabled = true
          if (popupCanSend) collector.btn.removeChild(popupCanSend)
          collector.btn.addChild(
            popupCantSend = popup(100,
              "Вы не можете отправить заявку!",
              "Не заполненны все обязательные поля!"
            )
          )
          collector.btn.element.classList.remove('make-btn-action-positive')
          collector.btn.element.classList.add('make-btn-action-negative')
        }
      })
      let modalForm
      collector.pushModifiers(
        Style.height("auto"),
        Style.minHeight("0"),
        With.style({overflow: "visible"}),
        makeIt.flexColumn,
        With.attr({flex: "0"}),
        Style.gap(6),
        make.Div(
          makeIt.flexRow,
          Style.gap(6),
          make.h1(data.form.label, With.style({alignSelf: "center", flex: 1})),
          picButton("close", "Закрыть", makeIt.act.negative, () => modalForm.close())
        ),
        make.Scrollbox(
          With.attr({flex: "999999"}),
          Style.gap(6),
          makeIt.flexColumn,
          ...data.fields.map(field =>
            formFieldElem(field, field.type)
          ),
        ),
        collector.btn = make.Button(
          makeIt.action,
          makeIt.act.positive,
          With.attr({flex: "0"}),
          With.text("Отправить"),
          With.attr({type: 'button'}),
          make.on.click(async () => {
            const data = collector.collect()
            const res = data.map(({ tag, ...rest }) => rest);
            const request = {
              data: res,
              form: formId
            }
            
            const newApplication = await qBase.at('applications').view().with(request).post()
            
            modalForm.close()
            
            paragraphNotice("Заявка отправлена!", make.color.lgreen)
            
            if (window.addApplicationToUserList) {
              window.addApplicationToUserList(newApplication)
            }
            
            if (typeof rebuildFoo === 'function') {
              setTimeout(rebuildFoo, 500)
            }
          })
        )
      )
      modalForm = make.Modal({blur: 8, autoHeight: true},
        makeIt.flexColumn,
        make.Div(
          makeIt.flexColumn,
          makeIt.content,
          With.style({border: "2px solid black", boxSizing: "border-box", overflow: "visible"}),
          Style.minHeight('0'),
          Style.height('auto'),
          collector,
        )
      )
      modalForm.build()
    }

    scrollbox.addModifiers(
      Style.height("100%"),
      ...Object.values(
        Object.values(cards).filter(elem => {
          return elem.cardContent.children[1].children.length >= 1
        })
      )
    )
    return [
      scrollbox,
    ]
}