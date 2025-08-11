export default (Component) => 
    
function (elementType, ...decorators) {
    const component = new Component(elementType);
    for (const decorator of decorators) {
        component.addDecorator(decorator);
    }
    return component;
};