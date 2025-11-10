export default function createTabs(Component, createComponent, makeWith, makeOn, Event) {
    class Tab {
        constructor(handler, first) {
            this._isFirst = first;
            this._handler = handler;
            this._header = null;
            this._content = null;
            this.onOpen = new Event({ret: this})
            this.onClose = new Event({ret: this})
        }

        header(...modifiers) {
            let addit = this._isFirst ? [makeWith.css('make-mark-active-tab')] : []
            const squareStyle = this._handler.squareTabs ? [makeWith.css('make-tab-button-square')] : []
            this._header = createComponent(
                'div',
                makeWith.css('make-tab-button'),
                ...squareStyle,
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
            if (this._handler._noAnimation) {
                const initialStyle = this._isFirst ? '' : 'display:none;';
                this._content = createComponent(
                    'div',
                    makeWith.css('make-tab-content'),
                    makeWith.attr({ style: initialStyle }),
                    ...modifiers
                );
            } else {
                const attrs = this._isFirst ? {} : { hidden: true };
                this._content = createComponent(
                    'div',
                    makeWith.css('make-tab-content'),
                    makeWith.attr(attrs),
                    ...modifiers
                );
            }
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
        constructor({scroll=false, noAnimation=false, squareTabs=false}={}, ...modifiers) {
            super('div');
            this.name = 'tabs'
            this.addModifiers(...modifiers);
            this.addDecorator(makeWith.css('make-tabs'));
            
            this._noAnimation = !!noAnimation;
            this.squareTabs = !!squareTabs;
            this.tabs = [];
            let addit = scroll ? [makeWith.css('make-tabs-menu-scroll'), ] : []
            this.menuContainer = createComponent('div', makeWith.css('make-tabs-menu'), ...addit);
            this.menuContainer.name = 'menu'
            this.contentContainer = createComponent('div', makeWith.css('make-tabs-content'));
            this.contentContainer.name = 'content'

            this.addChild(this.menuContainer);
            this.addChild(this.contentContainer);
            this.currentTab = null;

            this.onTabChange = new Event()
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
            this.currentTab?.onClose.emit(tab)
            
            if (this.currentTab && this.currentTab._content && this.currentTab._content.element) {
                if (this._noAnimation) {
                    this.currentTab._content.element.style.display = 'none';
                } else {
                    this.currentTab._content.element.setAttribute('hidden', '');
                }
                this.currentTab._header.element.classList.remove('make-mark-active-tab')
            }
            
            if (tab._content && tab._content.element) {
                if (this._noAnimation) {
                    tab._content.element.style.display = '';
                } else {
                    tab._content.element.removeAttribute('hidden');
                }
                tab._header.element.classList.add('make-mark-active-tab')
            }
            
            this.currentTab = tab;
            
            this.element.dispatchEvent(new CustomEvent('tabchange', {
                detail: { tab },
                bubbles: false
            }));
            this.onTabChange.emit(tab)
            this.currentTab.onOpen.emit(tab)
        }
    }
}
