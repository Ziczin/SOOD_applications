

export default (make, permissions, qBase) => {
  const qDocs = qBase.at("docs").view()

  function manualButton(txt, route, file) {
    return make.Div(
      make.it.marginOnHover,
      make.Button(
        make.it.littleDarker,
        make.it.redir,
        make.with.text(txt),
        make.on.click(async () => {
          let q =  qDocs.at(route).at(file).view()
          const url = q.route.build();
          const a = document.createElement('a');
          a.href = url;
          a.target = '_blank';
          document.body.appendChild(a);
          a.click();
          a.remove();
        })
      )
    )
  }
  function manualGroup(header, ...content) {
    return make.Div(
      make.it.marginOnHover,
      make.it.littleDarker,
      make.style.rounded(12),
      make.style.padding(6),
      make.it.flexColumn,
      make.style.gap(6),
      make.Paragraph(header, make.it.subtitleText),
      ...content
    )
  }

  return () => make.Div(
    make.it.flexColumn,
    make.style.gap(6),
    make.Separator(),
    make.Paragraph("Доступные руководства и файлы", make.it.textBold),
    manualGroup(
      "Общие",
      manualButton("Словарь терминов", "other", "termins"),
      manualButton("Вход и регистрация", "other", "register_login"),
    ),
    ...make.callif(
      permissions.includes("user"),
      () => manualGroup(
        "Пользователю",
        manualButton("Создание заявки", "user", "create_app")
      )
    ),
    ...make.callif(
      permissions.includes("moderator"),
      () => manualGroup(
        "Исполнителю",
        manualButton("Обработка заявкок", "moderator", "process_app")
      )
    ),
    ...make.callif(
      permissions.includes("admin"),
      () => manualGroup(
        "Администратору",
        manualButton("Формирование отчёта", "admin", "report"),
        manualButton("Управление сотрудниками", "admin", "users"),
        manualButton("Управление перечислениями", "admin", "enums"),
        manualButton("Управление наборами символов", "admin", "charsets"),
        manualButton("Управление шаблонами полей", "admin", "fields"),
        manualButton("Управление формами", "admin", "forms")
      )
    )
  )
}
