export default (Preferences, Flag) => {
    return {
        testCreation() {
            const prefs = new Preferences();
            return prefs.options !== undefined && 
                   prefs.listToParse !== undefined &&
                   prefs.flags !== undefined;
        },

        testObjectInitialization() {
            const prefs = new Preferences({ theme: 'dark', volume: 80 });
            return prefs.get('theme') === 'dark' && 
                   prefs.get('volume') === 80;
        },

        testArrayInitialization() {
            const prefs = new Preferences(['value1', 'value2']);
            return prefs.listToParse.length === 2 &&
                   prefs.listToParse[0] === 'value1' &&
                   prefs.listToParse[1] === 'value2';
        },

        testMixedArguments() {
            const prefs = new Preferences({ a: 1 }, ['b'], 'c');
            return prefs.get('a') === 1 &&
                   prefs.listToParse.includes('b') &&
                   prefs.listToParse.includes('c');
        },

        testFlags() {
            const flag = new Flag('experimental');
            const prefs = new Preferences(flag);
            return prefs.flags.experimental === true;
        },

        testGetExisting() {
            const prefs = new Preferences({ lang: 'ru' });
            return prefs.get('lang') === 'ru';
        },

        testGetDefault() {
            const prefs = new Preferences();
            return prefs.get('missing', 'default_value') === 'default_value';
        },

        testGetNull() {
            const prefs = new Preferences();
            return prefs.get('missing') === null;
        },

        testSetNew() {
            const prefs = new Preferences();
            prefs.set('newKey', 'newValue');
            return prefs.get('newKey') === 'newValue';
        },

        testSetNoOverwrite() {
            const prefs = new Preferences({ key: 'old' });
            prefs.set('key', 'new');
            return prefs.get('key') === 'old';
        },

        testSetForceOverwrite() {
            const prefs = new Preferences({ key: 'old' });
            prefs.set('key', 'new', true);
            return prefs.get('key') === 'new';
        },

        testParseString() {
            const prefs = new Preferences(['v1', 'v2']);
            prefs.parse('key1 key2');
            return prefs.get('key1') === 'v1' && 
                   prefs.get('key2') === 'v2';
        },

        testParseArray() {
            const prefs = new Preferences(['v1', 'v2']);
            prefs.parse(['key1', 'key2']);
            return prefs.get('key1') === 'v1' &&
                   prefs.get('key2') === 'v2';
        },

        testParseExtraNames() {
            const prefs = new Preferences(['v1']);
            prefs.parse('key1 key2');
            return prefs.get('key1') === 'v1' &&
                   prefs.get('key2') === null;
        },

        testParseOverwritesOld() {
            const prefs = new Preferences({ key: 'val' }, ['newVal']);
            prefs.parse('key');
            return prefs.get('key') === 'newVal';
        },

        testMultipleFlags() {
            const prefs = new Preferences(
                new Flag('f1'), 
                new Flag('f2', false)
            );
            return prefs.flags.f1 === true && 
                   prefs.flags.f2 === false;
        },

        testFlagsPriority() {
            const prefs = new Preferences(
                new Flag('admin'), 
                { user: 'John' }
            );
            return prefs.flags.admin === true && 
                   prefs.get('user') === 'John';
        },

        testFalseFlag() {
            const flag = new Flag('enabled', false);
            const prefs = new Preferences(flag);
            return prefs.flags.enabled === false;
        },

        testNotIgnoreNullUndefined() {
            const prefs = new Preferences(null, undefined).parse('a b');
            return prefs.listToParse.length === 2 &&
                   Object.keys(prefs.options).length === 2;
        },

        testSetChaining() {
            const prefs = new Preferences();
            const result = prefs.set('a', 1).set('b', 2);
            return result === prefs && 
                   prefs.get('a') === 1 && 
                   prefs.get('b') === 2;
        },

        testParseWithEmptyList() {
            const prefs = new Preferences();
            prefs.parse('key1 key2');
            return prefs.get('key1') === null &&
                   prefs.get('key2') === null;
        },

        testParseWithMoreListElements() {
            const prefs = new Preferences(['v1', 'v2', 'v3']);
            prefs.parse('key1 key2');
            return prefs.get('key1') === 'v1' &&
                   prefs.get('key2') === 'v2' &&
                   prefs.get('v3') === null;
        },

        testPrimitiveArguments() {
            const prefs = new Preferences('test', 123, true);
            return prefs.listToParse.includes('test') &&
                   prefs.listToParse.includes(123) &&
                   prefs.listToParse.includes(true);
        },

        testFlagRepr() {
            const flag = new Flag('test');
            const repr = flag.repr();
            return repr.test === true;
        },

        testMultipleObjects() {
            const prefs = new Preferences({ a: 1 }, { b: 2 });
            return prefs.get('a') === 1 && prefs.get('b') === 2;
        },

        testParseReturnThis() {
            const prefs = new Preferences(['v1']);
            const result = prefs.parse('key1');
            return result === prefs;
        }
    };
}