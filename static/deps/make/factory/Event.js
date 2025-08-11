export default (Decorator) =>
    
function (eventType, options = {}) {
    return (...handlers) => 
    new Decorator(
        component => {
            for (const handler of handlers) {
                component.element.addEventListener(eventType, handler, options);
            }
        },
        true
    );
} 