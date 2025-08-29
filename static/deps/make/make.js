import extension from './extension/_.js';
import factory from './factory/_.js';
import content from './content/_.js'
import core from './core/_.js'
import Preferences from './extension/wrapper/Preferences.js';
import other from './other/_.js';

const createComponent = factory.Component(extension.wrapper.Component);
const createDecorator = factory.Decorator(extension.wrapper.Decorator);
const createEvent = factory.Event(extension.wrapper.Decorator);

const makeWith = content.decorate.with(createDecorator);
const makeOn = content.decorate.on(createEvent);

const Tabs = content.prefab.Tabs(
    extension.wrapper.Component,
    createComponent,
    makeWith,
    makeOn
);

const Card = content.prefab.accordion.Card(extension.wrapper.Component, createComponent, makeWith, makeOn);
const Accordion = content.prefab.accordion.Accordion(
    extension.wrapper.Component, Card
);

window.make = (function() {
    console.log('Powered by make.js v0.0.5-dev')
    console.log(`
    CHANGE LOG
    - Some fixes on Query component allows to use 5 base REST methods
    - Card now gen it\`s own div-component
    - Rework Tabs component to use new chain syntax
    - Change versioning system
    - Added changelog :3
    `)

    return {
        other: other,
        with: makeWith,
        on: makeOn,
        it: content.decorate.it(makeWith.css),
        size: content.decorate.size(makeWith.css),
        color: content.decorate.color(makeWith.css),
        style: content.decorate.style(makeWith.style),
        Notice: content.prefab.Notice(core, extension.wrapper.Component),
        ...content.prefab.basic(createComponent),
        ...content.prefab.custom(
            createComponent, makeWith,
            content.decorate.inner(makeWith.css),
        ),
        Tabs: (...tabs) => new Tabs(...tabs),

        Accordion: (...cards) => new Accordion(...cards),
        Card: (...decorators) => new Card(...decorators),

        Preferences: (...args) => new Preferences(...args),
        'if': (condition, ...components) => condition ? components : [],
        case: (condition, ...components) => ({ condition, components }),
        switch: (...cases) => {
            for (const c of cases) {
                if (c.condition) {
                    return c.components;
                }
            }
            return [];
        },
        Query: (...params) => new extension.wrapper.Query(...params)
    };
})();