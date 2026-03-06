export default async () =>
{
  await import(`${window.make_url}/make.js`);

  const csrfObj = await make.Query('/api/csrf-token').get()
  const imp = (await import(`${window.prefab_url}/import.js`)).default(make)
  const popup = await imp(`${window.prefab_url}/popup.js`)
  const picButton = await imp(`${window.prefab_url}/pic_button.js`, popup, window.media_url)
  const paragraphNotice = await imp(`${window.prefab_url}/paragraph_notice.js`)
  
  const qBase = make.Query("/api")
                    .via({"X-CSRFToken": csrfObj.csrfToken})
                    .view()
  const me = await qBase.at('me').view().get()

  const buildAdminTab = await imp(`${window.dashboard_url}/admin.js`)
  const buildModerTab = await imp(`${window.dashboard_url}/moder.js`)
  const buildUserTab = await imp(`${window.dashboard_url}/user.js`)
  const buildUserAppsTab = await imp(`${window.dashboard_url}/userApps.js`)
  
  const departments = await qBase.at('departments').view().get()
  const deps = buildDepartmentNameMap(departments)
  const forms = await qBase.at('forms/visible').view().get()
  const statuses = await qBase.at('application-statuses').view().get()

  const permissions = me.permissions.filter(s => s !== 'proxy');
  let resultModer = null;
  
  let onOpenFooContainer = []
  if (permissions.includes('moderator')) {
    resultModer = await buildModerTab(
      qBase, me.department.id, statuses, popup, onOpenFooContainer, me, paragraphNotice);
  }

  const userApps = await buildUserAppsTab(qBase, me.id, statuses, popup, paragraphNotice)

  window.userAppsManager = userApps;
  window.getAndDrawUserApps = userApps.getAndDraw;
  window.addApplicationToUserList = function(newApplication) {
    if (window.userAppsManager && window.userAppsManager.addApplication) {
      window.userAppsManager.addApplication(newApplication);
    }
  }

  const tabs = make.Tabs({scroll: true}, make.style.height('100%'))
  .menu(
    make.with.style({flex: '0 0 auto'}),
    make.it.flexRow,
    make.it.gap10px,
    make.style.rounded(12),
    make.style.padding(8),
  );

  const buildUserTabWrapper = () => {
    return [
      make.Paragraph("Нажмите на панель с именем отдела, чтобы выбрать тип заявки",
        make.it.subtitleText
      ),
      ...buildUserTab(
        qBase, deps, forms, paragraphNotice, popup, window.getAndDrawUserApps, picButton)
    ]
  }
  document.getElementById('center-content').appendChild(
    make.Div(
      make.style.height("100%"),
      make.it.flexColumn,
      make.style.gap(6),
      make.with.style({overflowY: "hidden"}),
      ...make.callif(permissions.length === 0,
        () => make.h1("Перед началом работы верифицируйте аккаунт у администратора отдела или в отделе программирования.")
      ),
      ...make.callif(permissions.length > 0,
        () => {
          if (permissions.includes('user'))
            tabs.tab()
            .header(...getHeaderComponent("Мои заявки"))
            .content(
              make.it.flexColumn,
              userApps.handler
            );
            tabs.tab()
            .header(...getHeaderComponent("Создать заявку"))
            .content(
              make.it.flexColumn,
              ...buildUserTabWrapper()
            );
          if (permissions.includes('moderator'))
            tabs.tab()
            .onOpen.sub(() => onOpenFooContainer[0]())
            .header(...getHeaderComponent("Входящие заявки"))
            .content(
              ...(resultModer || [])
            );
          if (permissions.includes('admin'))
            tabs.tab()
            .header(...getHeaderComponent("Управление"))
            .content(
              ...buildAdminTab(qBase)
          );
          return tabs
        }
      )
    ).build()
  );

  function buildDepartmentNameMap(arr) {
    const map = {};
    for (let i = 0; i < arr.length; i++) {
        const item = arr[i];
        map[item.id] = item.name;
    }
    return map;
  }

  function getHeaderComponent(text) {
    return [
      make.style.rounded(12),
      make.style.padding(8),
      make.it.centered,
      make.it.textCentered,
      make.it.flex,
      make.Paragraph(text)
    ]
  }
}