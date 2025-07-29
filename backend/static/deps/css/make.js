// make.js
(function() {
    // Блок makeWith - функции-декораторы (с исправленными именами)
    const makeWith = {
        css: function(...classes) {
            return function(element) {
                classes.forEach(cls => cls && element.classList.add(cls));
                return element;
            };
        },
        text: function(text) {
            return function(element) {
                element.textContent = text;
                return element;
            };
        },
        attr: function(attributes) {
            return function(element) {
                Object.entries(attributes).forEach(([key, value]) => {
                    element.setAttribute(key, value);
                });
                return element;
            };
        },
        value: function(value) {
            return function(element) {
                element.setAttribute('value', value);
                return element;
            };
        },
        attrs: function(...attributes) {
            return function(element) {
                attributes.forEach((attr) => {
                    element.setAttribute(attr, '');
                });
                return element;
            };
        },
        click: function(handler) {
            return function(element) {
                element.addEventListener('click', handler);
                return element;
            };
        },
        children: function(...childs) {
            return function(element) {
                childs.forEach(child => {
                    if (child != undefined) {
                        element.appendChild(child);
                    }
                });
                return element;
            };
        }
    };

    // Блок make - создание элементов
    const make = {
        element: function(elementType, ...decorators) {
            const element = document.createElement(elementType);
            return decorators.reduce((el, decorator) => decorator(el) || el, element);
        },
        Div: function(...decorators) {
            return this.element('div', ...decorators);
        },
        Select: function(...decorators) {
            return this.element('select', ...decorators);
        },
        Input: function(...decorators) {
            return this.element('input', ...decorators);
        },
        Label: function(...decorators) {
            return this.element('label', ...decorators);
        },
        Paragraph: function(...decorators) {
            return this.element('p', ...decorators);
        },
        Button: function(...decorators) {
            return this.element('button',
                makeWith.attr({type: 'button'}),
                ...decorators
            );
        }
    };

    // Блок makeIt - модификация элементов
    const makeIt = {
        flexRow: function(element) {
            element.classList.add('flex-row');
            return element;
        },
        flexColumn: function(element) {
            element.classList.add('flex-column');
            return element;
        },
        gapped: function(element) {
            element.classList.add('gap-6px');
            return element;
        },
        formGroup: function(element) {
            element.classList.add('form-group', 'shady', 'margin-on-hover', 'recolor-on-hover');
            return element;
        },
        card: function(element) {
            element.classList.add('card');
            return element;
        },
        header: function(element) {
            element.classList.add('card-header');
            element.style.display = 'flex';
            element.style.justifyContent = 'space-between';
            element.style.alignItems = 'center';
            return element;
        },
        body: function(element) {
            element.classList.add('card-body');
            return element;
        },
        warning: function(element) {
            element.classList.add('btn', 'btn-warning', 'btn-sm');
            return element;
        },
        danger: function(element) {
            element.classList.add('btn', 'btn-danger', 'btn-sm');
            return element;
        },
        link: function(element) {
            element.classList.add('btn', 'btn-link');
            return element;
        },
        primary: function(element) {
            element.classList.add('btn', 'btn-primary');
            return element;
        }
    };

    // Добавляем необходимые стили
    const style = document.createElement('style');
    style.textContent = `
        .card { border-radius: 12px !important; border: 0 !important; }
        .card-header { padding: 0 !important; border: none !important; }
        .card-body { padding: 6px !important; background: #fff4 !important; }
        .btn { 
            border-radius: 12px; 
            border: none !important; 
            outline: none !important; 
            box-shadow: none !important;
            padding: 6px 12px;
            cursor: pointer;
        }
        .btn-primary { background-color: #007bff; color: white; }
        .btn-warning { background-color: #ffc107; color: black; }
        .btn-danger { background-color: #dc3545; color: white; }
        .btn-link { background: transparent; color: #007bff; text-decoration: underline; }
        .btn-sm { padding: 3px 6px; font-size: 0.875rem; }
    `;
    document.head.appendChild(style);

    // Экспортируем в глобальную область видимости
    window.makeWith = makeWith;
    window.make = make;
    window.makeIt = makeIt;
})();