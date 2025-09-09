export default function(createComponent) {
    return {
        Div: (...d) => createComponent('div', ...d),
        Link: (...d) => createComponent('a', ...d),
        Form: (...d) => createComponent('form', ...d),
        Input: (...d) => createComponent('input', ...d),
        Select: (...d) => createComponent('select', ...d),
        Button: (...d) => createComponent('button', ...d),
        TextArea: (...d) => createComponent('textarea', ...d),
        Preform: (...d) => createComponent('pre', ...d),
    }
}
