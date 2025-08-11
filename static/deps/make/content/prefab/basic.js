export default function(createComponent) {
    return {
        Div: (...d) => createComponent('div', ...d),
        Form: (...d) => createComponent('form', ...d),
        H1: (...d) => createComponent('h1', ...d),
        H2: (...d) => createComponent('h2', ...d),
        H3: (...d) => createComponent('h3', ...d),
        Select: (...d) => createComponent('select', ...d),
        Option: (...d) => createComponent('option', ...d),
        Input: (...d) => createComponent('input', ...d),
        Label: (...d) => createComponent('label', ...d),
        Paragraph: (...d) => createComponent('p', ...d),
        Button: (...d) => createComponent('button', ...d),
        Link: (...d) => createComponent('a', ...d),
    }
}
