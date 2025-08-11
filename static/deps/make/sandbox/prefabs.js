const makePrefab = {
    inputGroup: ({ text, type = 'text', placeholder = '', value = '' }) => createComponent(
        'div', 
        makeIt.formGroup, 
        makeIt.beautySelect, 
        createComponent(
            'label', 
            makeWith.text(text), 
            createComponent(
                'input',
                makeWith.attr({
                    placeholder,
                    value,
                    type
                })
            )
        )
    ),
    
    toggleButton: (textOn, textOff, ...decorators) => {
        let isToggled = false;
        
        const hiddenInput = createComponent(
            'input',
            makeWith.attr({
                type: 'hidden',
                value: 'false'
            })
        );
        
        const toggleHandler = () => {
            isToggled = !isToggled;
            const buttonElement = button.element;
               
            buttonElement.textContent = isToggled ? textOn : textOff;
            hiddenInput.element.value = String(isToggled);
            buttonElement.classList.toggle('make-toggle-active', isToggled);
            
            if (isToggled) {
                triggerActivate(buttonElement);
            } else {
                triggerDisactivate(buttonElement);
            }
        };
        
        const button = createComponent(
            'button',
            makeWith.text(textOff),
            makeWith.attr({ type: 'button' }),
            makeWith.css('make-button'),
            makeOn.click(toggleHandler),
            ...decorators
        );
        
        const container = createComponent(
            'div',
            makeWith.css('make-toggle-button-container'),
            button,
            hiddenInput
        );
        
        Object.assign(container, {
            toggle: () => button.element.click(),
            setState: (state) => {
                if (state !== isToggled) toggleHandler();
            },
            getState: () => isToggled,
            setName: (name) => {
                hiddenInput.element.name = name;
            }
        });
        
        return container;
    }
};

const triggerActivate = (element) => {
    const handlers = element._activateHandlers;
    if (handlers) {
        for (const handler of handlers) handler();
    }
};

const triggerDisactivate = (element) => {
    const handlers = element._disactivateHandlers;
    if (handlers) {
        for (const handler of handlers) handler();
    }
};