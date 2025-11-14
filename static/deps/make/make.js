import extension from './extension/_.js';
import factory from './factory/_.js';
import content from './content/_.js'
import core from './core/_.js'
import other from './other/_.js';
import meta from './meta.js';

extension.Component = extension.Component(extension.Decorator, extension.Event)
const createComponent = factory.Component(extension.Component);
const createDecorator = factory.Decorator(extension.Decorator);
const createHandler = factory.Handler(extension.Decorator);

const makeWith = content.decorate.with(createDecorator);
const makeOn = content.decorate.on(createHandler);

const Collector = content.prefab.Collector(
    extension.Component,
)

const Tabs = content.prefab.Tabs(
    extension.Component,
    createComponent,
    makeWith,
    makeOn,
    extension.Event
);

const Card = content.prefab.accordion.Card(
    extension.Component,
    createComponent,
    makeWith,
    makeOn,
    extension.Event
);

const Accordion = content.prefab.accordion.Accordion(
    extension.Component, Card
);

const Annotation = content.prefab.Annotation(core, extension.Component)

const Modal = content.prefab.Modal(extension.Component)

const noticeCollection = content.prefab.Notice(core, extension.Component, extension.Event, extension.Preferences)
other.closeCurrentNotice = noticeCollection.noticeHandler.closeActive.bind(noticeCollection.noticeHandler);
other.noticeHandler = noticeCollection.noticeHandler;
window.make = (() => {
    console.log(meta.greetings)
    console.log("Version: " + meta.version)
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
        limit: content.decorate.limit(createDecorator),

        //prefabs:
        ...content.prefab.basic(createComponent),
        ...content.prefab.custom(
            createComponent, makeWith,
            content.decorate.inner(makeWith.css),
        ),

        //Advanced prefabs:
        Tabs: (...mods) => new Tabs(...mods),
        Card: (...mods) => new Card(...mods),
        Accordion: (...cards) => new Accordion(...cards),
        UniqueNotice: noticeCollection.createUniqueNotice,
        Preferences: (...args) => new extension.Preferences(...args),
        Notice: noticeCollection.createNotice,
        Query: (...params) => extension.Query.new(...params),
        Collector: (...params) => new Collector(...params),
        Annotation: (params, ...mods) => new Annotation(params, ...mods),
        Modal: (params, ...mods) => new Modal(params, ...mods),
        meta: meta,
    };
})();