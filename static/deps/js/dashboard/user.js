function findDepartmentById(arr, id) {
    return arr.find(item => item.id === id) || null;
}

export default (make) =>
function dashboardUser(deps, forms, picButton, popup) {
    const scrollbox = make.Div(
        make.it.flexColumn,
        make.style.gap(6)
    )
    const cards = Object.fromEntries(
      Object.entries(deps).map(([key, value]) =>
        [key, make.Card(
          make.it.marginOnHover,
          make.with.style({border: "3px solid #ddd", backgroundColor: "#f5f5f5"}),
          make.style.padding(6),
          make.style.rounded(12),
        ).header(
          make.Paragraph(`Список заявок в: ${value}`),
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
    forms.forEach(element => {
      cards[element.department].cardContent.children[1].addChild(
        make.Div(
          make.it.marginOnHover,
          make.Button(
            make.it.redir,
            make.with.text(element.label || "Безымянная форма"),
            make.with.style({color: "#333"}),
            make.it.leftAlign,
            make.on.click(
              () => make.Notice([500, Infinity, 500, {weak: true}],
                make.Div(
                  make.style.padding(12),
                  make.color.mgray,
                  make.it.flexRow,
                  make.style.gap(6),
                  make.Paragraph("Представим, что тут действительно форма, но пока что это просто текст"),
                  picButton(
                    "close", "Закрыть",
                    make.it.act.negative,
                    () => make.other.closeCurrentNotice()
                  ),
                )
              )
            )
          )
        )
      )
    });

    scrollbox.addModifiers(
      ...Object.values(
        Object.values(cards).filter(elem => {
          console.log(elem)
          return elem.cardContent.children[1].children.length >= 1
      })
      )
    )
    return [
        scrollbox
    ]
}