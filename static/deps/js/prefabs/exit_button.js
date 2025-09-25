export default (make) =>
function exitWithNotice(
  text="Вернуться в аккаунт", style="back",
  location="/applications/dashboard/"){
  return make.Button(
    make.with.css("content", style, "flex"),
    make.with.text(text),
    make.on.click(() => window.location.href=location),
  )
}