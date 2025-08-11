// factory/_.js
import createComponent from './Component.js';
import createDecorator from './Decorator.js';
import createEvent from './Event.js';

export default {
    Component: createComponent,
    Decorator: createDecorator,
    Event: createEvent,
};
