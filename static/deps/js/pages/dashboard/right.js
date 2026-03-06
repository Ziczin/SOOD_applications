export default async () =>
{
  await import(`${window.make_url}/make.js`);
		
	const buildProxyTab = (await import(`${window.dashboard_url}/proxy.js`)).default(make);
	const me = await make.Query('/api/me').get();

	if (me.permissions.includes('proxy'))
		document.getElementById("right-content").appendChild(
			make.Div(
				make.it.content,
				make.style.padding(12),
				...(await buildProxyTab(me))
			).build()
		)
}