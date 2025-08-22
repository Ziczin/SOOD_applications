export default (Component) => 
    
function (elementType, ...modifiers) {
    const component = new Component(elementType, false);
    component.addModifiers(...modifiers).autoRebuild = true;
    return component;
};