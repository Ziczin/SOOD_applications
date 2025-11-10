export default (make) =>
function paragraphNotice(text, style, time = 500, weak=true) {
  if (!Array.isArray(text)) text = [text]
  return make.Notice([500, time, 500, text, {weak: weak}],
    make.Div(
      make.it.content,
      make.it.flexColumn,
      make.style.gap(6),
      style,
      ...text.map((el) => make.Paragraph(el))
    )
  )
}