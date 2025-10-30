export default (make, popup, media_url) =>
function picButton(pic, txt, style=[], onClick=()=>{}, outerStyle=[]) {
  if (!Array.isArray(style)) {
    style = [style, ]
  }
  if (!Array.isArray(outerStyle)) {
    outerStyle = [outerStyle, ]
  }
  return make.Div(
    ...outerStyle,
    make.Button(
      popup(800, txt),
      make.it.action,
      make.with.attr({type: "button"}),
      ...style,
      make.style.padding(6),
      make.Image(
        `${media_url}${pic}.png`,
        make.it.flex,
        make.with.style({width: "24px", height: "24px"}),
      ),
      make.on.click(onClick)
    )
  )
}
