import extension from './extension/_.js';
import factory from './factory/_.js';
import content from './content/_.js'
import core from './core/_.js'
import Preferences from './extension/wrapper/Preferences.js';

const createComponent = factory.Component(extension.wrapper.Component);
const createDecorator = factory.Decorator(extension.wrapper.Decorator);
const createEvent = factory.Event(extension.wrapper.Decorator);

const makeWith = content.decorate.with(createDecorator);
const makeOn = content.decorate.on(createEvent);

const Tab = content.prefab.tabs.Tab(extension.wrapper.Component, makeWith);
const TabContent = content.prefab.tabs.TabContent(extension.wrapper.Component);
const Tabs = content.prefab.tabs.Tabs(
    extension.wrapper.Component,
    createComponent,
    makeWith,
    makeOn
);

const Card = content.prefab.accordion.Card(extension.wrapper.Component, makeWith);
const CardContent = content.prefab.accordion.CardContent(extension.wrapper.Component);
const Accordion = content.prefab.accordion.Accordion(
    extension.wrapper.Component,
    extension.wrapper.Preferences,
    makeWith,
);

window.make = (function() {
    console.log('Powered by make.js')

    return {
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
        Tab: (title, ...decorators) => new Tab(title, ...decorators),
        TabContent: (...decorators) => new TabContent(...decorators),

        Accordion: (...cards) => new Accordion(...cards),
        Card: (title, ...decorators) => new Card(title, ...decorators),
        CardContent: (...decorators) => new CardContent(...decorators),

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
        }
    };
})();