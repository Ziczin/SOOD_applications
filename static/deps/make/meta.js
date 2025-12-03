let meta = {
    version: `0.4.2`,
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
    '0.4.2': `
v0.4.2-alpha
[2025.12.03]
- Added option 'on' to the 'Query' component, which allows executing a function after receiving a specific status/code
- Added 'submit' handler to the 'on' section for the corresponding event
- Minor style fixes
`,
    '0.4.1': `
v0.4.1-alpha
[2025.11.24]
- Added 'once()' method to 'Event': allows subscribing only once with auto-unsubscribe
- Added optional 'data-test-id' generator to 'Component': generates unique combinations by name or type and group
- Changed child component rendering system in 'Component': 'addModifiers()' no longer rebuilds component if not built before, added 'pushChild()' for adding without parent rebuild, added 'detachChild()' for detaching without destruction
- Reworked Collector: now checks all form fields for 'makeDataRequired' truthiness and triggers corresponding events
- Modified component factory: now can specify alias for 'data-test-id' as second parameter
- Added new constraint 'decimalPrecision' to 'limit' section: limits decimal places for number input fields
- Added 'config.js' for library configuration
- Added 'generateTestIds' parameter to 'config.js': enables unique combinations generation
- Removed 'view' method from 'Component' as unnecessary

`,
    '0.4.0': `
v0.4.0-alpha
[2025.11.14]
- Added new 'limit' section for applying constraints to components
- New constraint 'charactersWhiteList' in 'limit' section: allows setting allowed characters for input fields
- Added 'keydown' and 'paste' events to on section: 'inputTimeOut' now accepts events
- Added new input field type 'Checkbox' with corresponding styles
- Added events to 'Card' component: enabled by calling 'allowCustomEvents' method
- Added new 'Modal' component: modal window with default parameters
- Added 'noAnimation' mode for 'Tabs' component: completely disables rendering on inactive tabs for performance
- Fixed critical bug in 'Component' class: re-rendering now occurs after adding all passed components
- Added 'repeat(delay, method, func)' method to 'Query' component: sends requests at specified intervals
- Several style fixes

`,
    '0.3.1': `
v0.3.1-alpha
[2025.10.09]
- Added 'callif' for conditional function execution: fixes bug where normal if would build components that shouldn't be built
- Added 'callSwitch' with same fix for switch statements
- Some stylistic adjustments
- Partially fixed bug where 'Annotation' would remain visible after element removal
- Colors fixed

`,
    '0.3.0': `
v0.3.0-alpha
[2025.09.29]
- Renamed 'Event' factory to 'Handler'
- Added new 'Event' component: container for subscribed functions that can call them via 'emit()'
- Removed 'Applicable' as unnecessary: file structure updated
- 'Preferences' component can now parse list from constructor into object: 'parse()' accepts list of keys
- Added 'swap()' method to 'Component' class: swaps components in make.js component tree
- Completely rewritten 'Query' component: functionality preserved with cleaned codebase
- Reworked 'Notice' component: now supports weak notifications and requires values as list
- Some components now have their own 'Event' instances
- Added testing module for components
- Cleaned up comments
- Fixed several minor bugs

`,
    '0.2.2': `
v0.2.2-dev
- Rewrote 'Event' factory: can now pass factory returning multiple handlers and types
- Added 'SideSeparator' as analog of Separator
- Restored 'Tabs' component functionality: correct use of components as tab buttons and content
- Added 'splitLastN' function: allows signatures like '(...args, afterArgs)'
- Rewrote 'Query' component: query string construction now in where method
- Minor style tweaks

`,
    '0.2.1': `
v0.2.1-dev
- Fixed broken styles: 'make.style' now accepts string or number as pixel value

`,
    '0.2.0': `
v0.2.0-dev
- Added 'Annotation(time, ...components)' component: appears after hovering over attached component

`,
    '0.1.2': `
v0.1.2-dev
- Changed 'Query' component operation logic: now restores state to last checkpoint received via view()
- Improved meta.js file!

`,
    '0.1.0': `
v0.1.0-dev
- Added 'Collector' component: collects data from input fields by calling collect() method
- Added 'TextArea' component wrapping <textarea> tag
- Added 'Pre' component wrapping <pre> tag
- Made file structure changes

`,
    '0.0.6': `
v0.0.6-dev
- Reworked 'Notice': separated animations into open, idle, and close states
- Added 'closeCurrentNotice()' function: finds closest 'Notice' and closes it
- Added 'UniqueNotice(id, tIn, tIdle, tOut, ...dec)' component: prevents multiple notices with same id
- Separated changelog, version, and greetings from 'make.js' file

`,
    '0.0.5': `
v0.0.5-dev
- Fixed 'Query' component to support 5 basic REST methods
- 'Card' now generates its own div component
- Reworked 'Tabs' component to use new chain syntax
- Changed versioning system
- Added changelog :3

`
}

meta.changes = (v) => {console.log(changelog[v]); return `...`}
meta.changelog = (v) => {console.log(Object.values(changelog).join('\n')); return `...`}
meta.versions = Object.keys(changelog)
meta.last = changelog[meta.version]

export default meta