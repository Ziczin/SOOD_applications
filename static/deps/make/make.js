import extension from './extension/_.js';
import factory from './factory/_.js';
import content from './content/_.js'
import core from './core/_.js'

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

window.make = (function() {
    console.log('Powered by make.js')

    return {
        with: makeWith,
        on: makeOn,
        it: content.decorate.it(makeWith.css),
        size: content.decorate.size(makeWith.css),
        color: content.decorate.color(makeWith.css),
        Notice: content.prefab.Notice(core, extension.wrapper.Component),
        ...content.prefab.basic(createComponent),
        ...content.prefab.custom(createComponent, content.decorate.inner(makeWith.css)),
        Tabs: (...tabs) => new Tabs(...tabs),
        Tab: (title, ...decorators) => new Tab(title, ...decorators),
        TabContent: (...decorators) => new TabContent(...decorators),
        // query: query
    };
})();