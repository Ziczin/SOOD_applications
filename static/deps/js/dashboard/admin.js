export default (make) =>
function(qBase) {
  const btns = [
    {
      text: 'Управление формами',
      loc: '/applications/forms-manager/',
    },
    {
      text: 'Управление сотрудниками',
      loc: '/applications/users-manager/',
    },
    {
      text: 'Управление перечислениями',
      loc: '/applications/enums-manager/',
    },
    {
      text: 'Управление наборами символов',
      loc: '/applications/charsets-manager/',
    },
    {
      text: 'Управление шаблонами полей',
      loc: '/applications/fields-manager/',
    },
  ]
  const now = new Date();
  const startOfThisMonth = new Date(now.getFullYear(), now.getMonth(), 1);
  const startOfNextMonth = new Date(now.getFullYear(), now.getMonth() + 1, 1);

  function formatDateForInput(date){
    const y = date.getFullYear();
    const m = String(date.getMonth()+1).padStart(2,'0');
    const d = String(date.getDate()).padStart(2,'0');
    return `${y}-${m}-${d}`;
  }

  let isoThis = make.Input(
    make.with.attr({
      type: "date", value: formatDateForInput(startOfThisMonth)
    }),
  )
  let isoNext = make.Input(
    make.with.attr({
      type: "date", value: formatDateForInput(startOfNextMonth)
    }),
  )
  return [
    make.it.flexColumn,
    make.style.gap(6),
    make.h1("Статистика по отделу"),
    make.Div(
      make.with.style({flex: 0}),
      make.it.flexRow,
      make.style.gap(6),
      make.Paragraph('С', make.with.style({alignSelf: "center"})),
      isoThis,
      make.Paragraph('по', make.with.style({alignSelf: "center"})),
      isoNext,
    ),
    make.Button(
      make.it.action,
      make.it.act.positive,
      make.with.text("Сформировать отчёт"),
      make.with.attr({type: "button"}),
      make.on.click(async () => {
        let q = qBase.at('report').where({
          dateFrom: isoThis.element.value,
          dateTo: isoNext.element.value
        }).view()
        const url = q.route.build() + q.query.build();
        const a = document.createElement('a');
        a.href = url;
        a.target = '_blank';
        document.body.appendChild(a);
        a.click();
        a.remove();
      })
    ),
    make.Separator(6, make.style.rounded(12), make.color.lgray),
    make.Separator(0),
    make.h1("Управление"),
    ...btns.map(btn =>
      make.Div(
        make.it.marginOnHover,
        make.Button(
          make.it.redir,
          make.with.text(btn.text),
          make.on.click(() => {
            window.location.href = btn.loc
          })
        )
      ),
    ),
    make.Separator(6, make.style.rounded(12), make.color.lgray),
  ]
}