export default function(createComponent) {
    return {
        Div: (...d) => createComponent('div', ...d),
        Form: (...d) => createComponent('form', ...d),
        Select: (...d) => createComponent('select', ...d),
        Option: (...d) => createComponent('option', ...d),
        Input: (...d) => createComponent('input', ...d),
        Label: (...d) => createComponent('label', ...d),
        Button: (...d) => createComponent('button', ...d),
        Link: (...d) => createComponent('a', ...d),
    }
}
