export default (make) =>
function popup (...text) {
  let time = 1500
  if (typeof text[0] === "number") { [time, ...text] = text }
  if (text[0] instanceof Array) { text = text[0] }
  return make.Annotation(
    time,
    make.Div(
      make.it.popup,
      ...text.map(txt => make.Paragraph(txt))
    )
  )
}
