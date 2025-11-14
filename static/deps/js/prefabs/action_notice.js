export default (make) => 
function actionNotice({
  question=[],
  action=()=>{},
  cancel=()=>{},
  confirmText="Удалить",
  cancelText="Отмена"
  }) {
  if (typeof question === 'string') {question = [question]}
  if (Array.isArray(question)) {
    if (question.every(item => typeof item === 'string')) {
      question = question.map((item) => make.Paragraph(item))
    }
  }
  make.Notice([500, Infinity, 500, "actionNotice"],
    make.Div(
      make.it.flexColumn,
      make.style.gap(6),
      make.it.contented,
      ...question,
      make.Div(
        make.it.flexRow,
        make.style.gap(6),
        make.Button(
          make.it.action,
          make.it.act.negative,
          make.with.text(confirmText),
          make.with.style({flex: 1}),
          make.on.click(() => {
            action()
            make.other.closeCurrentNotice()
          })
        ),
        make.Button(
          make.it.action,
          make.it.act.alternative,
          make.with.text(cancelText),
          make.with.style({flex: 1}),
          make.on.click(() => {
            cancel()
            make.other.closeCurrentNotice()
          })
        ),
      )
    )
  )
}