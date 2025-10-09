export default (make) =>
function paragraphNotice(text, style) {
  return make.Notice([500, 500, 500, text, {weak: true}],
    make.Div(
      make.it.content,
      style,
      make.Paragraph(text)
    )
  )
}