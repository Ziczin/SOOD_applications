export default (make) =>
function dashboardUser(qBase, deps, forms, paragraphNotice, popup, rebuildFoo, picButton) {
    const scrollbox = make.Scrollbox(
        make.it.flexColumn,
        make.style.gap(6),
    )
    const cards = Object.fromEntries(
      Object.entries(deps).map(([key, value]) =>
        [key, make.Card(
          make.it.marginOnHover,
          make.with.style({border: "3px solid #ddd", backgroundColor: "#f5f5f5"}),
          make.style.padding(6),
          make.style.rounded(12),
        ).header(
          make.Paragraph(value),
          popup("Нажмите чтобы развернуть список форм данного отдела"),
          make.color.lgray,
          make.style.margin(-8),
          make.style.padding(6),
          make.style.rounded(12),
          make.with.style({border: "3px solid #ddd"}),
        ).content(
          make.Separator(6),
          make.style.height('100%'),
          make.Div(
            make.with.style({paddingTop: "8px"}),
            make.style.rounded(12),
            make.it.flexColumn,
            make.style.gap(6),
          )
        )]
      )
    );
    forms.forEach(form => {
      cards[form.department].cardContent.children[1].addChild(
        make.Div(
          make.it.marginOnHover,
          make.Button(
            make.it.redir,
            make.with.text(form.label || "Безымянная форма"),
            make.with.style({color: "#333"}),
            make.it.leftAlign,
            make.on.click(async () => formModal(form.id)),
            popup(400, "Нажмите, чтобы открыть окно заполнения формы")
          )
        )
      )
    });

    function formFieldElem(field, type) {
      const wrapper = make.Div(
        make.it.marginOnHover,
        make.style.rounded(12),
        make.style.padding(12),
        ...make.callif(
          field.required && field.type !== 'checkbox',
          () => make.with.css("have-status-REJECTED")
        ),
        ...make.callif(!field.required || field.type === 'checkbox', () => make.color.lgray)
      )
      if (type !== "checkbox") {
        wrapper.addModifiers(
          make.it.flexColumn,
          make.style.gap(6),
          make.Paragraph(field.label),
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
              make.with.attr({id: field.id}),
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
          make.it.flexRow,
          make.style.gap(6),
          make.Checkbox(make.with.attr({id: field.id})),
          make.Paragraph(field.label, make.with.style({alignSelf: "center"})),
        )
      }
      return wrapper
    }

    function dateFieldElem(type) {
      return make.Input(
        make.with.attr({type: type})
      )
    }

    function textFieldElem(field) {
      return make.Input(
        make.with.attr({placeholder: field.placeholder || ''})
      )
    }

    function textareaFieldElem(field) {
      return make.TextArea(
        make.with.attr({
			placeholder: field.placeholder || ''
		}),
		make.with.style({
			resize: "vertical"
		})
      )
    }

    function numberFieldElem(field) {
      return make.Input(
        make.with.attr({type: "number"}),
        ...make.callif(field.decimals,
          () => make.limit.decimalPrecision(field.decimals)
        ),
        ...make.callif(field.minimum,
          () => make.with.attr({min: field.minimum})
        ),
        ...make.callif(field.maximum,
          () => make.with.attr({max: field.maximum})
        ),

      )
    }

    function charsetFieldElem(field) {
      return make.Input(
        make.with.attr({placeholder: field.placeholder || ''}),
        make.limit.charactersWhiteList(field.charset.preview),
        popup(2000, "Это ограниченное поле, доступные символы:",
          field.charset.humanized_preview
        ),
        ...make.callif(field.charset.min_length,
          () => make.with.attr({minlength: field.charset.min_length})
        ),  
        ...make.callif(field.charset.max_length,
          () => make.with.attr({maxlength: field.charset.max_length})
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
        make.style.height("auto"),
        make.style.minHeight("0"),
        make.with.style({overflow: "visible"}),
        make.it.flexColumn,
        make.with.attr({flex: "0"}),
        make.style.gap(6),
        make.Div(
          make.it.flexRow,
          make.style.gap(6),
          make.h1(data.form.label, make.with.style({alignSelf: "center", flex: 1})),
          picButton("close", "Закрыть", make.it.act.negative, () => modalForm.close())
        ),
        make.Scrollbox(
          make.with.attr({flex: "999999"}),
          make.style.gap(6),
          make.it.flexColumn,
          ...data.fields.map(field =>
            formFieldElem(field, field.type)
          ),
        ),
        collector.btn = make.Button(
          make.it.action,
          make.it.act.positive,
          make.with.attr({flex: "0"}),
          make.with.text("Отправить"),
          make.with.attr({type: 'button'}),
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
        make.it.flexColumn,
        make.Div(
          make.it.flexColumn,
          make.it.content,
          make.with.style({border: "2px solid black", boxSizing: "border-box", overflow: "visible"}),
          make.style.minHeight('0'),
          make.style.height('auto'),
          collector,
        )
      )
      modalForm.build()
    }

    scrollbox.addModifiers(
      make.style.height("100%"),
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