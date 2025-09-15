import extension from './extension/_.js';
import factory from './factory/_.js';
import content from './content/_.js'
import core from './core/_.js'
import Preferences from './extension/wrapper/Preferences.js';
import other from './other/_.js';
import meta from './meta.js';

const createComponent = factory.Component(extension.wrapper.Component);
const createDecorator = factory.Decorator(extension.wrapper.Decorator);
const createEvent = factory.Event(extension.wrapper.Decorator);

const makeWith = content.decorate.with(createDecorator);
const makeOn = content.decorate.on(createEvent);

const Collector = content.prefab.Collector(
    extension.wrapper.Component,
)

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

const Annotation = content.prefab.Annotation(core, extension.wrapper.Component)

const noticeCollection = content.prefab.Notice(core, extension.wrapper.Component)
other.closeCurrentNotice = noticeCollection.noticeHandler.closeActive.bind(noticeCollection.noticeHandler);
window.make = (function() {
    console.log(meta.greetings)
    console.log(meta.version)
    console.log(meta.subgreetings)

    return {
        
        //logic:
        other: other,
        ...other.conditions,

        //decorators:
        with: makeWith,
        on: makeOn,
        it: content.decorate.it(makeWith.css),
        size: content.decorate.size(makeWith.css),
        color: content.decorate.color(makeWith.css),
        style: content.decorate.style(makeWith.style),

        //prefabs:
        ...content.prefab.basic(createComponent),
        ...content.prefab.custom(
            createComponent, makeWith,
            content.decorate.inner(makeWith.css),
        ),

        //Advanced prefabs:
        Tabs: (...tabs) => new Tabs(...tabs),
        Card: (...decorators) => new Card(...decorators),
        Accordion: (...cards) => new Accordion(...cards),
        UniqueNotice: noticeCollection.createUniqueNotice,
        Preferences: (...args) => new Preferences(...args),
        Notice: noticeCollection.createNotice,
        Query: (...params) => new extension.wrapper.Query(...params),
        Collector: (...params) => new Collector(...params),
        Annotation: (t, ...params) => new Annotation(t, ...params),
        meta: meta,
    };
})();