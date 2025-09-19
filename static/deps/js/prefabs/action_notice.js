export default (make) => 
function actionNotice({
  question=[],
  action=()=>{},
  confirmText="Удалить",
  cancelText="Отмена"
  }) {
  if (typeof question === 'string') {question = [question]}
  if (Array.isArray(question)) {
    if (question.every(item => typeof item === 'string')) {
      question = question.map((item) => make.Paragraph(item))
    }
  }
  make.UniqueNotice("actionNotice", 500, Infinity, 500,
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
          make.on.click(() => {
            action(),
            make.other.closeCurrentNotice()
          })
        ),
        make.Button(
          make.it.action,
          make.it.act.alternative,
          make.with.text(cancelText),
          make.on.click(() => {
            make.other.closeCurrentNotice()
          })
        ),
      )
    )
  )
}