export default function createTabs(Component, createComponent, makeWith, makeOn) {
    return class Tabs extends Component {
        constructor(...tabs) {
            super('div');
            this.addDecorator(makeWith.css('make-tabs'));
            
            if (!tabs.every(tab => tab.constructor.name === 'Tab')) {
                throw new Error('Tabs can only contain Tab elements');
            }
            
            this.tabs = tabs;
            this.menuContainer = createComponent('div', makeWith.css('make-tabs-menu'));
            this.contentContainer = createComponent('div', makeWith.css('make-tabs-content'));
            
            this.addChild(this.menuContainer, this.contentContainer);
            this.currentActiveIndex = 0;
        }

        build(force = false) {
            super.build(force);
            
            // Очищаем контейнеры
            this.menuContainer.element.innerHTML = '';
            this.contentContainer.element.innerHTML = '';
            
            // Строим вкладки
            this.tabs.forEach((tab, index) => {
                // Кнопка вкладки
                const button = tab.build();
                button.classList.add('make-tab-button');
                button.setAttribute('aria-controls', `tab-content-${index}`);
                button.setAttribute('id', `tab-button-${index}`);
                button.addEventListener('click', () => this.activateTab(index));
                
                // Контент вкладки
                const content = tab.tabContent.build();
                content.classList.add('make-tab-content');
                content.setAttribute('id', `tab-content-${index}`);
                content.setAttribute('role', 'tabpanel');
                content.setAttribute('aria-labelledby', `tab-button-${index}`);
                content.hidden = index !== this.currentActiveIndex;
                
                if (index === this.currentActiveIndex) {
                    button.classList.add('active');
                    button.setAttribute('aria-selected', 'true');
                } else {
                    button.setAttribute('aria-selected', 'false');
                }
                
                this.menuContainer.element.appendChild(button);
                this.contentContainer.element.appendChild(content);
            });
            
            return this.element;
        }

        activateTab(index) {
            if (this.currentActiveIndex === index) return;
            
            // Обновляем предыдущую вкладку
            const prevButton = this.menuContainer.element.children[this.currentActiveIndex];
            const prevContent = this.contentContainer.element.children[this.currentActiveIndex];
            prevButton.classList.remove('active');
            prevButton.setAttribute('aria-selected', 'false');
            prevContent.hidden = true;
            
            // Активируем новую вкладку
            this.currentActiveIndex = index;
            const newButton = this.menuContainer.element.children[index];
            const newContent = this.contentContainer.element.children[index];
            newButton.classList.add('active');
            newButton.setAttribute('aria-selected', 'true');
            newContent.hidden = false;
            
            // Генерируем событие
            this.element.dispatchEvent(new CustomEvent('tabchange', {
                detail: { index },
                bubbles: true
            }));
        }
    };
}