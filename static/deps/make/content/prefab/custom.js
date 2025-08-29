export default function(createComponent, makeWith) {
    return {
        Separator: (size = 8, ...decorators) => {
            return createComponent('div', 
                makeWith.style({ 'margin-top': `${size}px` }),
                ...decorators
            );
        },
        Scrollbox: (...d) => createComponent('div', makeWith.css('make-scrollbox'), ...d),
        Paragraph: (txt, ...d) => typeof txt === 'string'
            ? createComponent('p', makeWith.text(txt), ...d)
            : createComponent('p', ...d),
        Span: (txt, ...d) => typeof txt === 'string'
            ? createComponent('span', makeWith.text(txt), ...d)
            : createComponent('span', ...d),
        h1: (txt, ...d) => typeof txt === 'string'
            ? createComponent('h1', makeWith.text(txt), ...d)
            : createComponent('h1', ...d),
        h2: (txt, ...d) => typeof txt === 'string'
            ? createComponent('h2', makeWith.text(txt), ...d)
            : createComponent('h2', ...d),
        h3: (txt, ...d) => typeof txt === 'string'
            ? createComponent('h3', makeWith.text(txt), ...d)
            : createComponent('h3', ...d),
        Image: (src, ...d) => typeof src === 'string'
            ? createComponent('img', makeWith.attr({src: src}), ...d)
            : createComponent('img', ...d),
        Label: (txt, ...d) => typeof txt === 'string'
            ? createComponent('label', makeWith.text(txt), ...d)
            : createComponent('label', ...d),
        Option: (txt, value, ...d) => typeof txt === 'string'
            ? createComponent('option', makeWith.text(txt), makeWith.attr({value: value}), ...d)
            : createComponent('option', ...d),
    }
}
