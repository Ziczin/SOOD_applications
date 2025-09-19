export default (make) =>
function popup (time = 1500, text = []) {
  if (typeof time === 'string' || Array.isArray(time)) {
    text = time;
    time = 1500;
  }
  if (typeof text === 'string') text = [text];

  return make.Annotation(
    time,
    make.Div(
      make.it.popup,
      ...text.map(txt => make.Paragraph(txt))
    )
  )
}