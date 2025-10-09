import test from './test/_.js'

import extension from './extension/_.js'

test.all("Preferences",
    test.preferences(
        extension.Preferences(extension.Flag),
        extension.Flag
    ), true
)