import {query} from '../core/query.js';

window.make = (function() {
    return {
        with: makeWith,
        it: makeIt,
        on: makeOn,
        color: makeColor,
        inner: makeInner,
        prefab: makePrefab,
        element: createComponent,
        Div: (...d) => createComponent('div', ...d),
        Form: (...d) => createComponent('form', ...d),
        H1: (...d) => createComponent('h1', ...d),
        H2: (...d) => createComponent('h2', ...d),
        H3: (...d) => createComponent('h3', ...d),
        Select: (...d) => createComponent('select', ...d),
        Option: (...d) => createComponent('option', ...d),
        Input: (...d) => createComponent('input', ...d),
        Label: (...d) => createComponent('label', ...d),
        Paragraph: (...d) => createComponent('p', ...d),
        Button: (...d) => createComponent('button', ...d),
        Link: (...d) => createComponent('a', ...d),
        Separator: (...d) => createComponent('div', makeInner.separator, ...d),
        Scrollbox: (...d) => createComponent('div', makeInner.scrollbox, ...d),
        Tabs: Tabs,
        Notice: createNotice,
        query: query
    };
})();
