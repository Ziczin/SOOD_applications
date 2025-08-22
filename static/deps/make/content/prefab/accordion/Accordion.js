export default function createAccordion(Component, Card) {
  return class Accordion extends Component {
    constructor(...modifiers) {
      super('div');
      this.addModifiers(...modifiers)
      this.cards = new Set();
    }

    addChild(child) {
      super.addChild(child);
      if (child instanceof Card) {
        child.bindAccordion(this);
      }

      return this;
    }

    closeAllCardsExcept(exceptCard) {
      this.children.filter(
        item => item instanceof Card
      ).forEach(card => {
          if (card !== exceptCard) {
            card.closeCard();
          }
        }
      );
    }
  };
}