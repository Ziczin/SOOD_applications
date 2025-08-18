export default function createAccordion(Component, Preferences, makeWith) {
    return class Accordion extends Component {
        constructor(...args) {
            super('div');
            this.addDecorator(makeWith.css('make-accordion'));
            
            let preferences;
            let cards;
            if (args.length > 0 && args[0] instanceof Preferences) {
                preferences = args[0];
                cards = args.slice(1);
            } else {
                preferences = new Preferences({});
                cards = args;
            }
            
            this.preferences = preferences
                .set('isMulti', false)
                .set('timeOpen', 300)
                .set('timeClose', 300);
            
            if (cards.length > 0) {
                this.addChild(...cards);
            }
            
            this.currentActiveIndices = new Set();
            this.previousActiveIndices = new Set();
            this.contentElements = [];
            this.isBuilding = false;
            this.transitioning = new Set();
            this.pendingIndex = null;
            this.autoRebuild = false; // Отключаем автоматический rebuild
        }

        build(force = false) {
            if (this.destroyed) return null;
            if (this.isBuilding) return this.element;
            
            this.isBuilding = true;
            try {
                if (!this.element) {
                    this.element = document.createElement(this.elementType);
                    this.element.classList.add('make-accordion');
                }
                
                if (force || this.contentElements.length === 0) {
                    this.element.innerHTML = '';
                    this.contentElements = [];
                    this._buildAllCards();
                }
                
                this.updateStates();
                return this.element;
            } finally {
                this.isBuilding = false;
            }
        }

        _buildAllCards() {
            this.children.forEach((card, index) => {
                this._buildSingleCard(card, index);
            });
        }

        _buildSingleCard(card, index) {
            if (!card || !card.cardContent) return;
            
            const cardId = `accordion-content-${index}`;
            const headerButton = card.build();
            headerButton.classList.add('make-accordion-header');
            headerButton.setAttribute('aria-controls', cardId);
            headerButton.setAttribute('aria-expanded', 'false');
            headerButton.id = headerButton.id || `accordion-header-${index}`;
            
            if (!headerButton._accordionListener) {
                const listener = () => this.toggleCard(index);
                headerButton.addEventListener('click', listener);
                headerButton._accordionListener = listener;
            }
            
            const content = card.cardContent.build();
            content.classList.add('make-accordion-content');
            content.setAttribute('id', cardId);
            content.setAttribute('role', 'region');
            content.setAttribute('aria-labelledby', headerButton.id);
            content.style.overflow = 'hidden';
            content.style.maxHeight = '0';
            content.style.opacity = '0';
            
            this.contentElements[index] = content;
            this.element.appendChild(headerButton);
            this.element.appendChild(content);
        }

        addChild(...items) {
            const startIndex = this.children.length;
            const result = super.addChild(...items);
            
            if (this.element) {
                items.forEach((card, offset) => {
                    const index = startIndex + offset;
                    this._buildSingleCard(card, index);
                    this.contentElements[index] = card.cardContent.element;
                });
            }
            
            return result;
        }

        updateStates() {
            if (this.isBuilding || this.destroyed) return;
            const isMulti = this.preferences.get('isMulti', false);
            const timeOpen = this.preferences.get('timeOpen', 300);
            const timeClose = this.preferences.get('timeClose', 300);
            
            const previousActive = new Set(this.previousActiveIndices);
            this.previousActiveIndices = new Set(this.currentActiveIndices);
            
            this.children.forEach((card, index) => {
                if (!card || !this.contentElements[index]) return;
                
                const headerButton = card.element || card.build();
                const content = this.contentElements[index];
                const isActive = this.currentActiveIndices.has(index);
                const wasActive = previousActive.has(index);
                
                if (isActive === wasActive) return;
                
                headerButton.setAttribute('aria-expanded', isActive.toString());
                
                if (!isMulti && isActive && wasActive) {
                    this._closeCard(index, content, timeClose);
                } else if (isActive) {
                    this._openCard(index, content, timeOpen);
                } else {
                    this._closeCard(index, content, timeClose);
                }
            });
        }

        _openCard(index, content, timeOpen) {
            if (this.transitioning.has(index)) return;
            
            content.style.maxHeight = '0';
            content.style.opacity = '0';
            
            void content.offsetHeight;
            
            this.transitioning.add(index);
            content.style.transition = `max-height ${timeOpen}ms ease-in-out, opacity ${timeOpen}ms ease-in-out`;
            
            const targetHeight = content.scrollHeight;
            content.style.maxHeight = targetHeight + 'px';
            content.style.opacity = '1';
            
            const handleTransitionEnd = () => {
                content.removeEventListener('transitionend', handleTransitionEnd);
                if (this.currentActiveIndices.has(index)) {
                    content.style.transition = 'none';
                    content.style.maxHeight = 'none';
                }
                this.transitioning.delete(index);
            };
            
            content.addEventListener('transitionend', handleTransitionEnd);
        }

        _closeCard(index, content, timeClose) {
            if (this.transitioning.has(index)) return;
            
            content.style.maxHeight = content.scrollHeight + 'px';
            content.style.opacity = '1';
            
            void content.offsetHeight;
            
            this.transitioning.add(index);
            content.style.transition = `max-height ${timeClose}ms ease-in-out, opacity ${timeClose}ms ease-in-out`;
            content.style.maxHeight = '0';
            content.style.opacity = '0';
            
            const handleTransitionEnd = () => {
                content.removeEventListener('transitionend', handleTransitionEnd);
                this.transitioning.delete(index);
            };
            
            content.addEventListener('transitionend', handleTransitionEnd);
        }

        toggleCard(index) {
            if (this.transitioning.has(index) || this.isBuilding) return;
            const isActive = this.currentActiveIndices.has(index);
            const isMulti = this.preferences.get('isMulti', false);
            
            if (isActive) {
                this.currentActiveIndices.delete(index);
            } else {
                if (!isMulti) {
                    this.previousActiveIndices = new Set(this.currentActiveIndices);
                    this.currentActiveIndices.clear();
                }
                this.currentActiveIndices.add(index);
            }
            this.updateStates();
        }
    };
}