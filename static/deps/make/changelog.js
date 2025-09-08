import { version } from "react";

export default {
    version: `v0.0.6-dev`,
    changelog: `
CHANGE LOG
v0.0.6
- Rework Notice: separate animation to open, idle and close states
- Added other.closeCurrentNotice() function, which finds closest Notice and closes it
- Added UniqueNotice(id, tIn, tIdle, tOut, ...dec) component, which not allow add to handler multiple notices with same id

v0.0.5
- Some fixes on Query component allows to use 5 base REST methods
- Card now gen it\`s own div-component
- Rework Tabs component to use new chain syntax
- Change versioning system
- Added changelog :3
`
}