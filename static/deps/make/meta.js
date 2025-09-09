let meta = {
    version: `v0.1.1-dev`,
    greetings: `Powered by make.js`,
    subgreetings: 'Call window.make.meta.help() for more info',
    help: () => console.log(`
window.make.meta.<...>
- help - this message
- version - full version of make.js
- versions - list of versions
- changes('version') - changelog of specified version
- changelog() - full changelog
`)
}

let changelog = {
    '0.1.1': `
v0.1.1-dev
- Improved meta.js file!
`,
    '0.1.0': `
v0.1.0-dev
- Added Collector component, which collects data from input fields, selects, and textareas by calling the collect() method
- Added TextArea component that wraps the <textarea> tag
- Added Pre component that wraps the <pre> tag
- Made some file structure changes
`,
    '0.0.6': `
v0.0.6-dev
- Reworked Notice: separated animations into open, idle, and close states
- Added other.closeCurrentNotice() function, which finds the closest Notice and closes it
- Added UniqueNotice(id, tIn, tIdle, tOut, ...dec) component, which does not allow adding multiple notices with the same id to the handler
- Separated changelog, version, and greetings from the 'make.js' file
`,
    '0.0.5': `
v0.0.5-dev
- Fixed Query component to support 5 basic REST methods
- Card now generates its own div component
- Reworked Tabs component to use the new chain syntax
- Changed versioning system
- Added changelog :3
`
}

meta.changes = (v) => console.log(changelog[v])
meta.changelog = (v) => console.log(Object.values(changelog).join('\n'))
meta.versions = Object.keys(changelog)

export default meta
