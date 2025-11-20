export default (Component) => 
function (elementType, ...modifiers) {
    let component
    if (Array.isArray(elementType)) {
        const [type, name] = elementType;
        component = new Component(type, false);
        component.name = name
    }
    else {
        component = new Component(elementType, false);
    }
    component.addModifiers(...modifiers).autoRebuild = true;
    return component;
};