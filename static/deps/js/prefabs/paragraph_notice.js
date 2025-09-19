export default (make) =>
function paragraphNotice(text, style) {
  return make.Notice(500, 500, 500,
    make.Div(
      make.it.content,
      style,
      make.Paragraph(text)
    )
  )
}