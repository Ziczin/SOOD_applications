export default (make, role) =>
function enumsManager() {
    const tabs = make.Tabs(make.style.height('100%'))
    .menu(
      make.it.flexRow,
      make.it.gap10px,
      make.style.rounded(12),
      make.style.padding(8),
    );
}