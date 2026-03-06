export default async () =>
{
  await import(`${window.make_url}/make.js`);
  const imp = (await import(`${window.prefab_url}/import.js`)).default(make)
  const backButton = await imp(`${window.prefab_url}/exit_button.js`)
  const popup = await imp(`${window.prefab_url}/popup.js`)
  const picButton = await imp(`${window.prefab_url}/pic_button.js`, popup, window.media_url);

  const csrfObj = await make.Query('/api/csrf-token').get()
  const qBase = make.Query("/api").via({"X-CSRFToken": csrfObj.csrfToken}).view();
  const me = await qBase.at("me").view().get()
  
  const basicManual = await imp(`${window.manual_url}/basic_manual.js`, popup, picButton);
  const mainManual = await imp(`${window.manual_url}/main_manual.js`, ["user", "moderator", "admin"], qBase)
  
  document.getElementById('manual-button').appendChild(basicManual(mainManual).build())
  document.getElementById("left-exit-button").appendChild(backButton().build())

}