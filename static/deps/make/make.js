window.make = (function() {
    class Component {
        constructor(element, type) {
            this.element = element;
            this.type = type;
            this.children = [];
            this.parent = null;
        }
        
        appendChild(child) {
            if (child instanceof Component) {
                child.parent = this;
                this.element.appendChild(child.element);
                this.children.push(child);
            } else {
                this.element.appendChild(child);
            }
            return this;
        }
        
        insertChildAt(child, index) {
            if (index < 0 || index > this.children.length) return this;
            if (child instanceof Component) {
                const refNode = index < this.children.length ? this.children[index].element : null;
                this.element.insertBefore(child.element, refNode);
                this.children.splice(index, 0, child);
                child.parent = this;
            }
            return this;
        }
        
        removeChild(child) {
            const index = this.children.indexOf(child);
            if (index !== -1) {
                this.element.removeChild(child.element);
                this.children.splice(index, 1);
                child.parent = null;
            }
            return this;
        }
        
        removeChildAt(index) {
            if (index >= 0 && index < this.children.length) {
                const child = this.children[index];
                this.element.removeChild(child.element);
                this.children.splice(index, 1);
                child.parent = null;
            }
            return this;
        }
        
        getChildAt(index) {
            return this.children[index];
        }
        
        replaceChild(newChild, oldChild) {
            const index = this.children.indexOf(oldChild);
            if (index !== -1) {
                this.element.replaceChild(newChild.element, oldChild.element);
                this.children[index] = newChild;
                newChild.parent = this;
                oldChild.parent = null;
            }
            return this;
        }
        
        clearChildren() {
            while (this.element.firstChild) {
                this.element.removeChild(this.element.firstChild);
            }
            this.children.forEach(child => child.parent = null);
            this.children = [];
            return this;
        }
        
        applyDecorators(...decorators) {
            decorators.forEach(decorator => decorator(this.element));
            return this;
        }
    }

    const makeWith = {
        css: (...classes) => element => {
            classes.forEach(cls => cls && element.classList.add(cls));
            return element;
        },
        text: text => element => {
            element.textContent = text;
            return element;
        },
        attr: attributes => element => {
            Object.entries(attributes).forEach(([key, value]) => element.setAttribute(key, value));
            return element;
        },
        value: value => element => {
            element.setAttribute('value', value);
            return element;
        },
        attrs: (...attributes) => element => {
            attributes.forEach(attr => element.setAttribute(attr, ''));
            return element;
        },
        click: handler => element => {
            element.addEventListener('click', handler);
            return element;
        },
        childs: (...chs) => element => {
            chs.forEach(child => child != undefined && element.appendChild(child instanceof Component ? child.element : child));
            return element;
        },
        tab: (title, ...items) => {
            const decorators = [];
            const contentItems = [];
            
            items.forEach(item => {
                if (typeof item === 'function') {
                    decorators.push(item);
                } else {
                    if (Array.isArray(item)) {
                        contentItems.push(...item);
                    } else {
                        contentItems.push(item);
                    }
                }
            });
            
            return {
                type: 'tab',
                title: title,
                content: contentItems,
                decorators: decorators,
                parent: null
            };
        },
        content: (...elements) => elements,
        csrf: token => element => {
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = token;
            element.appendChild(csrfInput);
            return element;
        }
    };

    const makeColor = {
        error: e => e.classList.add('make-color-error'),
    };

    const makeOn = {
        hover: (...handlers) => element => {
            handlers.forEach(handler => element.addEventListener('mouseenter', handler));
            return element;
        },
        dehover: (...handlers) => element => {
            handlers.forEach(handler => element.addEventListener('mouseleave', handler));
            return element;
        },
        click: (...handlers) => element => {
            handlers.forEach(handler => element.addEventListener('click', handler));
            return element;
        },
        focus: (...handlers) => element => {
            handlers.forEach(handler => element.addEventListener('focus', handler));
            return element;
        },
        defocus: (...handlers) => element => {
            handlers.forEach(handler => element.addEventListener('blur', handler));
            return element;
        },
    };

    function createComponent(elementType, ...decorators) {
        const element = document.createElement(elementType);
        const component = new Component(element, elementType);
        decorators.forEach(decorator => typeof decorator === 'function' && decorator(component.element));
        return component;
    }

    const makeIt = {
        textItalic: e => e.classList.add('make-text-italic'),
        leftAlign: e => e.classList.add('make-text-align-left'),
        simpleLink: e => e.classList.add('make-simple-link'),
        gap10px: e => e.classList.add('make-gap-10px'),
        gap6px: e => e.classList.add('make-gap-6px'),
        flexRow: e => e.classList.add('make-flex-row'),
        flexColumn: e => e.classList.add('make-flex-column'),
        gapped: e => e.classList.add('gap-6px'),
        formGroup: e => e.classList.add('make-form-group'),
        beautySelect: e => e.classList.add('make-beauty-select'),
        card: e => e.classList.add('card'),
        body: e => e.classList.add('card-body'),
        warning: e => e.classList.add('btn', 'btn-warning', 'btn-sm'),
        danger: e => e.classList.add('btn', 'btn-danger', 'btn-sm'),
        link: e => e.classList.add('btn', 'btn-link'),
        primary: e => e.classList.add('btn', 'btn-primary'),
        onConfirmationMargin: e => e.classList.add('make-confirmation-margin'),
    };

    const makeInner = {
        separator: e => e.classList.add('make-block-separator')
    }

    const Tabs = (...args) => {
        const containerDecorators = [];
        const tabs = [];
        
        args.forEach(arg => {
            if (arg && arg.type === 'tab') {
                tabs.push(arg);
            } else if (typeof arg === 'function') {
                containerDecorators.push(arg);
            }
        });
        
        const tabsContainer = createComponent('div', ...containerDecorators, makeWith.css('make-tabs'));
        const menuContainer = createComponent('div', makeWith.css('make-tabs-menu'));
        const contentContainer = createComponent('div', makeWith.css('make-tabs-content'));
        tabsContainer.appendChild(menuContainer).appendChild(contentContainer);
        
        tabs.forEach((tab, index) => {
            const tabId = Math.random().toString(36).substring(2, 10);
            const button = createComponent('button',
                makeWith.text(tab.title),
                makeWith.attr({ id: `tab-${tabId}` }),
                makeWith.css('make-tab-button'),
                ...tab.decorators
            );
            
            const contentDiv = createComponent('div', makeWith.attr({ id: `content-${tabId}` }));
            
            if (tab.content) {
                tab.content.forEach(item => {
                    if (Array.isArray(item)) {
                        item.forEach(subItem => {
                            if (subItem instanceof Component) {
                                contentDiv.appendChild(subItem);
                            } else if (subItem instanceof Node) {
                                contentDiv.element.appendChild(subItem);
                            }
                        });
                    } else {
                        if (item instanceof Component) {
                            contentDiv.appendChild(item);
                        } else if (item instanceof Node) {
                            contentDiv.element.appendChild(item);
                        }
                    }
                });
            }
            
            if (index !== 0) contentDiv.element.setAttribute('hidden', '');
            else button.element.classList.add('active');
            
            button.element.addEventListener('click', () => {
                contentContainer.children.forEach(child => child.element.setAttribute('hidden', ''));
                contentDiv.element.removeAttribute('hidden');
                menuContainer.children.forEach(child => child.element.classList.remove('active'));
                button.element.classList.add('active');
            });
            
            menuContainer.appendChild(button);
            contentContainer.appendChild(contentDiv);
        });
        
        return tabsContainer;
    };

    async function query(route, method, data = null) {
        method = method.toUpperCase();
        const validMethods = ['GET', 'POST', 'PUT', 'DELETE'];
        
        if (!validMethods.includes(method)) {
            throw new Error(`Invalid HTTP method: ${method}`);
        }

        const options = {
            method: method,
            headers: {}
        };

        // Для GET-запросов добавляем параметры в URL
        if (method === 'GET' && data) {
            const params = new URLSearchParams(data).toString();
            route = `${route}?${params}`;
        }
        // Для других методов добавляем данные в тело
        else if (data) {
            options.headers['Content-Type'] = 'application/json';
            options.body = JSON.stringify(data);
        }

        const response = await fetch(route, options);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    return {
        with: makeWith,
        it: makeIt,
        on: makeOn,
        color: makeColor,
        element: createComponent,
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
        Separator: (...d) => createComponent('div', makeInner.separator, ...d),
        Tabs: Tabs,
        query: query
    };
})();