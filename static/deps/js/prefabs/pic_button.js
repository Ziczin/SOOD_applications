export default (make, popup, media_url) =>
function picButton(pic, txt, style=[], onClick=()=>{}) {
  if (!Array.isArray(style)) {
    style = [style, ]
  }
  return make.Div(
    make.Button(
      popup(800, txt),
      make.it.action,
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
