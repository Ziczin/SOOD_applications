let meta = {
    version: `0.3.1`,
    greetings: `Powered by make.js`,
    subgreetings: 'Call window.make.meta.help() for more info',
    help: () => console.log(`
window.make.meta.<...>
- help() - this message
- last() - last changelog
- version - version of make.js
- versions - list of versions
- changes('version') - changelog of specified version
- changelog() - full changelog
`)
}

let changelog = {
    '0.3.1': `
v0.3.1-alpha
- callif - Conditional function execution; fixes a bug where a normal if would build components that shouldn't be built
- callSwitch - same fix for switch
- some stylistic adjustments
- partially fixed a bug where an annotation would remain visible after an element was removed
- colors fixed
`,
    '0.3.0': `
v0.3.0-alpha
- Renamed Event factory to Handler
- Added new Event component — a container for subscribed functions that can call them all via emit(), which also accepts parameters. Subscription via sub(fn), unsubscription via unsub(fn)
- Removed Applicable as it was unnecessary; file structure updated
- Preferences component can now parse a list produced by the constructor into an object. Method parce() accepts a list of keys
- Added swap() method to Component class to swap components in the make.js component tree
- Completely rewritten Query component; functionality preserved but codebase cleaned up. Separate entities now store body, headers, query string and route
- Reworked Notice component; it now supports "weak" notifications (default weak=false) that hide when a new notice enters the queue. All settings moved to a Preferences instance. New syntax requires passing values as a list, e.g. make.Notice([500, 500, 500, "this-is-unique-id", {weak: true}], ...someStuff)
- Some components now have their own Event instances
- Added a testing module for components
- Cleaned up comments
- Fixed several minor bugs
`,
    '0.2.2': `
v0.2.2-dev
- Rewrote Event factory: you can now pass a factory that returns multiple handlers and their types, enabling more complex interactions
- Added SideSeparator — an analogue of Separator
- Restored Tabs component functionality: you can now correctly use components as tab buttons and as tab content
- Added splitLastN function, which allows signatures like (...args, afterArgs)
- Rewrote Query component: query string construction now happens in the where method, similar to with
- Minor style tweaks
`,
    '0.2.1': `
v0.2.1-dev
- Fixed some broken styles. Now make.style can accept either a string or a number; a number is interpreted as a pixel value (px)
`,
    '0.2.0': `
v0.2.0-dev
- Added Annotation(time ...components) component, which appears in time milliseconds after hovering over the component to which it is attached
`,
    '0.1.2': `
v0.1.2-dev
- Changed Query component operation logic: now it restores the state to the last checkpoint received via view() using get, post, put, patch, delete
`,
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

meta.changes = (v) => {console.log(changelog[v]); return `...`}
meta.changelog = (v) => {console.log(Object.values(changelog).join('\n')); return `...`}
meta.versions = Object.keys(changelog)
meta.last = changelog[meta.version]

export default meta
