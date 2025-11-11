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
            make.on.click(async () => formNotice(form.id))
          )
        )
      )
    });

    async function formNotice(formId) {
      let data = await qBase.at('forms').at(formId).at('data').view().get()
      let collector = make.Collector()
      let modalForm
      collector.addModifiers(
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
          ...data.fields.map(field => {
            const wrapper = make.Div(
              make.it.marginOnHover,
              make.color.lgray,
              make.style.rounded(12),
              make.style.padding(12),
              make.it.flexColumn,
              make.style.gap(6),
              make.Paragraph(field.label)
            );
            if (field.type === "enum") {
              wrapper.addChild(
                make.Select(
                  make.with.attr({ id: field.id }),
                  make.OptionPlaceholder(`--- выберите элемент--- `),
                  ...field.enums.map(enu => make.Option(enu.value, enu.id))
                )
              );
            } else {
              wrapper.addChild(
                make.Input(make.with.attr({ id: field.id }))
              );
            }
            return wrapper;
          }),
        ),
        make.Button(
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
            await qBase.at('applications').view().with(request).post()
            await rebuildFoo()
            modalForm.close()
            paragraphNotice("Заявка отправлена!", make.color.lgreen)
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