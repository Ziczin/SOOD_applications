function Tabs(...args) {
    const [tabs, containerDecorators] = args.reduce((acc, arg) => {
        arg?.type === 'tab' 
            ? acc[0].push(arg) 
            : typeof arg === 'function' && acc[1].push(arg);
        return acc;
    }, [[], []]);

    const tabsContainer = createComponent(
        'div',
        ...containerDecorators,
        makeWith.css('make-tabs')
    );
    
    const menuContainer = createComponent('div', makeWith.css('make-tabs-menu'));
    const contentContainer = createComponent('div', makeWith.css('make-tabs-content'));
    tabsContainer.append(menuContainer, contentContainer);

    let currentActiveIndex = 0;
    const tabElements = [];

    tabs.forEach((tab, index) => {
        const button = createComponent(
            'button',
            makeWith.text(tab.title),
            makeWith.attr({
                'type': 'button',
                'aria-controls': `tab-content-${index}`,
                'aria-selected': 'false'
            }),
            makeWith.css('make-tab-button'),
            ...(tab.decorators || []),
            makeOn.click(() => activateTab(index))
        );

        const content = createComponent(
            'div',
            makeWith.css('make-tab-content'),
            makeWith.attr({
                'id': `tab-content-${index}`,
                'role': 'tabpanel',
                'aria-labelledby': `tab-button-${index}`
            })
        );

        if (tab.content) {
            content.append(...tab.content.flat().filter(Boolean));
        }

        button.addDecorator(new Decorator(element => {
            if (index === currentActiveIndex) {
                element.classList.add('active');
                element.setAttribute('aria-selected', 'true');
            }
        }));

        content.addDecorator(new Decorator(element => {
            element.hidden = index !== currentActiveIndex;
        }));

        menuContainer.append(button);
        contentContainer.append(content);
        tabElements.push({ button, content });
    });

    const activateTab = (index) => {
        if (currentActiveIndex === index) return;

        const prevButton = tabElements[currentActiveIndex].button;
        const prevContent = tabElements[currentActiveIndex].content;
        
        if (prevButton.element) {
            prevButton.element.classList.remove('active');
            prevButton.element.setAttribute('aria-selected', 'false');
        }
        if (prevContent.element) prevContent.element.hidden = true;

        currentActiveIndex = index;
        const newButton = tabElements[index].button;
        const newContent = tabElements[index].content;
        
        if (newButton.element) {
            newButton.element.classList.add('active');
            newButton.element.setAttribute('aria-selected', 'true');
        }
        if (newContent.element) newContent.element.hidden = false;

        if (tabsContainer.element) {
            tabsContainer.element.dispatchEvent(
                new CustomEvent('tabchange', {
                    detail: { index },
                    bubbles: true
                })
            );
        }
    };

    return tabsContainer;
}