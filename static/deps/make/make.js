import extension from './extension/_.js';
import factory from './factory/_.js';
import content from './content/_.js'
import core from './core/_.js'

const createComponent = factory.Component(extension.wrapper.Component);
const createDecorator = factory.Decorator(extension.wrapper.Decorator);
const createEvent = factory.Event(extension.wrapper.Decorator);

const makeWith = content.decorate.with(createDecorator);

window.make = (function() {
    console.log('Powered by make.js')

    return {
        with: makeWith,
        on: content.decorate.on(createEvent),
        it: content.decorate.it(makeWith.css),
        size: content.decorate.size(makeWith.css),
        color: content.decorate.color(makeWith.css),
        Notice: content.prefab.Notice(core, extension.wrapper.Component),
        ...content.prefab.basic(createComponent),
        ...content.prefab.custom(createComponent, content.decorate.inner(makeWith.css)),
        // Tabs: Tabs,
        // query: query
    };
})();