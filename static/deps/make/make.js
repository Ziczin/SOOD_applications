import extension from './extension/_.js';
import factory from './factory/_.js';
import content from './content/_.js'
import core from './core/_.js'
import other from './other/_.js';
import meta from './meta.js';
import config from './config.js';

const Event = extension.Event
const Decorator = extension.Decorator
const Component = extension.Component(Decorator, Event, config.generateTestIds)
const Preferences = extension.Preferences

const decoratorFactory = factory.Decorator(Decorator);
const componentFactory = factory.Component(Component);
const handlerFactory = factory.Handler(Decorator);

const makeWith = content.decorate.with(decoratorFactory);
const makeOn = content.decorate.on(handlerFactory);

const Collector = content.prefab.Collector(Component, Event)

const customComponentSetup = [Component, componentFactory, makeWith, makeOn, Event]

const Tabs = content.prefab.Tabs(...customComponentSetup);
const Card = content.prefab.accordion.Card(...customComponentSetup);

const Accordion = content.prefab.accordion.Accordion(Component, Card);
const Annotation = content.prefab.Annotation(core, Component)
const Modal = content.prefab.Modal(Component)

const noticeCollection = content.prefab.Notice(core, Component, Event, Preferences)

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
        limit: content.decorate.limit(decoratorFactory),

        //prefabs:
        ...content.prefab.basic(componentFactory),
        ...content.prefab.custom(
            componentFactory, makeWith,
            content.decorate.inner(makeWith.css),
        ),

        //Advanced prefabs:
        Tabs: (...mods) => new Tabs(...mods),
        Card: (...mods) => new Card(...mods),
        Accordion: (...cards) => new Accordion(...cards),
        UniqueNotice: noticeCollection.createUniqueNotice,
        Preferences: (...args) => new Preferences(...args),
        Notice: noticeCollection.createNotice,
        Query: (...params) => extension.Query.new(...params),
        Collector: (...params) => new Collector(...params),
        Annotation: (params, ...mods) => new Annotation(params, ...mods),
        Modal: (params, ...mods) => new Modal(params, ...mods),
        meta: meta,
    };
})();