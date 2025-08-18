export default function createCard(Component, makeWith) {
    return class Card extends Component {
        constructor(title, cardContent, ...decorators) {
            super('button');
            if (!cardContent || !(cardContent.constructor.name === 'CardContent')) {
                throw new Error('Card requires exactly one CardContent element');
            }
            
            this.title = title;
            this.cardContent = cardContent;
            this.addDecorator(makeWith.text(title));
            this.addDecorator(makeWith.attr({ type: 'button' }));
            decorators.forEach(d => this.addDecorator(d));
        }
    };
}