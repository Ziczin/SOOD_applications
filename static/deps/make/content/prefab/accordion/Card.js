export default function createCard(Component, createComponent, makeWith, makeOn) {
  return class Card extends Component {
    constructor(...modifiers) {
      super('div');
      this.cardHeader = null;
      this.cardContent = null;
      this.state = 'closed';
      this.addModifiers(...modifiers);
      this.accordion = null;

      this._onHeaderClick = (event) => {
        event.stopPropagation();
        
        if (this.state === 'opening' || this.state === 'closing') return;
        this.toggle();
      };
      
      this.addDecorator(makeWith.css('make-card'));
    }

    bindAccordion(accordion) {
      this.accordion = accordion;
    }

    header(...modifiers) {
      this.cardHeader = createComponent(
        'div',
        makeWith.css('make-card-header'),
        makeOn.click(this._onHeaderClick),
        ...modifiers)
      this.addChild(this.cardHeader);
      return this;
    }

    content(...modifier) {
      this.cardContent = createComponent('div', ...modifier)
      this.addChild(this.cardContent);
      this.setupContentAnimation();
      return this;
    }

    setupContentAnimation() {
      if (!this.cardContent?.element) return;
      
      const el = this.cardContent.element;
      el.classList.add('make-card-content');
      
      if (this.state === 'closed') {
        el.style.height = '0px';
        el.style.pointerEvents = 'none';
      }
      
      const onTransitionEnd = (event) => {
        event.stopPropagation();
        this.finishAnimation();
      };
      
      el.addEventListener('transitionend', onTransitionEnd);
    }

    finishAnimation() {
      if (!this.cardContent?.element) return;
      
      const el = this.cardContent.element;
      
      if (this.state === 'opening') {
        this.state = 'open';
        el.style.pointerEvents = 'auto';
        el.style.height = 'auto';
      } else if (this.state === 'closing') {
        this.state = 'closed';
        el.style.pointerEvents = 'none';
      }
    }

    toggle() {
      if (this.state === 'opening' || this.state === 'closing') return;
      
      if (this.state === 'closed') {
        this.openCard();
      } else {
        this.closeCard();
      }
    }

    openCard() {
      if (this.state !== 'closed' || !this.cardContent?.element) return;
      
      this.accordion?.closeAllCardsExcept(this);
      this.state = 'opening';
      const el = this.cardContent.element;
      
      el.style.pointerEvents = 'none';
      
      const startHeight = el.getBoundingClientRect().height;
      el.style.height = startHeight + 'px';
      
      void el.offsetHeight;
      el.style.height = el.scrollHeight + 'px';
    }

    closeCard() {
      if (
        this.state === 'closed' ||
        !this.cardContent?.element
      ) return;
      
      this.state = 'closing';
      const el = this.cardContent.element;
      
      el.style.pointerEvents = 'none';
      const startHeight = el.getBoundingClientRect().height;
      el.style.height = startHeight + 'px';
      
      void el.offsetHeight;
      el.style.height = '0px';
    }
  };
}