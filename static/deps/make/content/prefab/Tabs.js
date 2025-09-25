export default function createTabs(Component, createComponent, makeWith, makeOn) {
    class Tab {
        constructor(handler, first) {
            this._isFirst = first;
            this._handler = handler;
            this._header = null;
            this._content = null;
        }
        
        header(...modifiers) {
            let addit = this._isFirst ? [makeWith.css('make-mark-active-tab')] : []
            this._header = createComponent(
                'div',
                makeWith.css('make-tab-button'),
                makeOn.click(() => {
                    this._handler.activateTab(this)
                }),
                ...addit,
                ...modifiers
            );
            this._handler.menuContainer.addChild(this._header);
            return this;
        }
        
        content(...modifiers) {
            this._content = createComponent(
                'div',
                makeWith.css('make-tab-content'),
                makeWith.attr(this._isFirst ? {} : {hidden: true}),
                ...modifiers
            );
            this._handler.contentContainer.addChild(this._content);
            return this._handler;
        }
        
        tab(placeholder) {
            return this._handler.tab();
        }
        build() {
            return this._handler.build()
        }
    }

    return class Tabs extends Component {
        constructor({scroll=false}={}, ...modifiers) {
            super('div');
            this.name = 'tabs'
            this.addModifiers(...modifiers);
            this.addDecorator(makeWith.css('make-tabs'));
            
            this.tabs = [];
            let addit = scroll ? [makeWith.css('make-tabs-menu-scroll'), ] : []
            this.menuContainer = createComponent('div', makeWith.css('make-tabs-menu'), ...addit);
            this.menuContainer.name = 'menu'
            this.contentContainer = createComponent('div', makeWith.css('make-tabs-content'));
            this.contentContainer.name = 'content'

            this.addChild(this.menuContainer);
            this.addChild(this.contentContainer);
            this.currentTab = null;
        }
        
        menu(...modifiers) {
            this.menuContainer.addModifiers(...modifiers)
            return this
        }

        content(...modifiers) {
            this.contentContainer.addModifiers(...modifiers)
            return this
        }

        tab(placeholder) {
            let isFirst = this.tabs.length === 0
            const tab = new Tab(this, isFirst);
            this.tabs.push(tab);
            if (isFirst) {this.activateTab(tab)};
            return tab;
        }
        
        activateTab(tab) {
            if (this.currentTab === tab) return;
            
            if (this.currentTab && this.currentTab._content && this.currentTab._content.element) {
                this.currentTab._content.element.setAttribute('hidden', '');
                this.currentTab._header.element.classList.remove('make-mark-active-tab')
            }
            
            if (tab._content && tab._content.element) {
                tab._content.element.removeAttribute('hidden');
                tab._header.element.classList.add('make-mark-active-tab')
            }
            
            this.currentTab = tab;
            
            this.element.dispatchEvent(new CustomEvent('tabchange', {
                detail: { tab },
                bubbles: false
            }));
        }
    }
}
