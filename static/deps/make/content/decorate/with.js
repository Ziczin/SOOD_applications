export default (createDecorator) =>
{
    return {
        css: createDecorator(
            (component, ...classes) => {
                for (const cls of classes) {
                    if (cls) component.element.classList.add(cls);
                }
            }, true
        ),
        
        style: createDecorator(
            (component, styles) => {
                if (styles && typeof styles === 'object') {
                    Object.assign(component.element.style, styles);
                }
            }, true
        ),
        
        text: createDecorator(
            (component, text) => {
                component.element.textContent = text;
            }, true
        ),
        
        attr: createDecorator(
            (component, attributes) => {
                for (const [key, value] of Object.entries(attributes)) {
                    component.element.setAttribute(key, value);
                }
            }, true
        ),
        
        value: createDecorator(
            (component, value) => {
                component.element.value = value;
            }, true
        ),
        
        attrs: createDecorator(
            (component, ...attributes) => {
                for (const attr of attributes) {
                    component.element.setAttribute(attr, '');
                }
            }, true
        ),
        
        csrf: createDecorator(
            (component, token) => {
                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrfmiddlewaretoken';
                csrfInput.value = token;
                component.element.appendChild(csrfInput);
            }, true
        )
    }
}