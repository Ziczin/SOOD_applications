export default (make) =>
function (
  text="Вернуться в аккаунт",
  location="/applications/dashboard/") {
  return make.Div(
    make.it.marginOnHover,
    make.Button(
      make.it.action,
      make.it.leftAlign,
      make.it.act.neutral,
      make.with.text(text),
      make.on.click(() => window.location.href=location),
    )
  )
}