export default (Decorator) => {
    function add(component, eventType, handler) {
        component.element.addEventListener(eventType, handler, { passive: true });
    }
    return {
        basic: (eventType) => (handler) =>
        new Decorator(
            component => add(component, eventType, handler), true
        ),
        custom :(factory) =>
        (...params) => {
            const handlers = factory(...params)
            return new Decorator(
                component => {
                    for (const h of handlers){
                        add(component, h.eventType, h.handler)
                    }
                }, true
            )
        }
    }
}