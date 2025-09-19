export default (make) =>
function exitWithNotice({
  text="Вернуться в аккаунт", style="back",
  noticeText="Все несохранённые изменения будут утеряны",
  confirmText="Выйти",
  cancelText="Отмена",
  location="/applications/dashboard/"
}){
  return make.Button(
    make.with.css("content", style, "flex"),
    make.with.text(text),
    make.on.click(() =>
      make.Notice(500, Infinity, 500,
        make.Div(
          make.it.content,
          make.it.flexColumn,
          make.style.gap(6),
          make.Paragraph(noticeText),
          make.Div(
            make.it.flexRow,
            make.style.gap(6),
            make.Button(
              make.it.action,
              make.it.act.negative,
              make.with.text(confirmText),
              make.on.click(() => window.location.href=location),
            ),
            make.Button(
              make.it.action,
              make.it.act.alternative,
              make.with.text(cancelText),
              make.on.click(() => make.other.closeCurrentNotice()),
            )
          )
        )
      )
    )
  )
}