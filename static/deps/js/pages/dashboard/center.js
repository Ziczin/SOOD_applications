export default async () =>
{
  await import(`${window.make_url}/make.js`);

  const Style = make.style
  const makeIt = make.it
  const Paragraph = make.Paragraph
  const With = make.with

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

  const tabs = make.Tabs({scroll: true}, Style.height('100%'))
  .menu(
    With.style({flex: '0 0 auto'}),
    makeIt.flexRow,
    makeIt.gap10px,
    Style.rounded(12),
    Style.padding(8),
  );

  const buildUserTabWrapper = () => {
    return [
      Paragraph("Нажмите на панель с именем отдела, чтобы выбрать тип заявки",
        makeIt.subtitleText
      ),
      ...buildUserTab(
        qBase, deps, forms, paragraphNotice, popup, window.getAndDrawUserApps, picButton)
    ]
  }
  document.getElementById('center-content').appendChild(
    make.Div(
      Style.height("100%"),
      makeIt.flexColumn,
      Style.gap(6),
      With.style({overflowY: "hidden"}),
      ...make.callif(permissions.length === 0,
        () => make.h1("Перед началом работы верифицируйте аккаунт у администратора отдела или в отделе программирования.")
      ),
      ...make.callif(permissions.length > 0,
        () => {
          if (permissions.includes('user'))
            tabs.tab()
            .header(...getHeaderComponent("Мои заявки"))
            .content(
              makeIt.flexColumn,
              userApps.handler
            );
            tabs.tab()
            .header(...getHeaderComponent("Создать заявку"))
            .content(
              makeIt.flexColumn,
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
      Style.rounded(12),
      Style.padding(8),
      makeIt.centered,
      makeIt.textCentered,
      makeIt.flex,
      Paragraph(text)
    ]
  }
}