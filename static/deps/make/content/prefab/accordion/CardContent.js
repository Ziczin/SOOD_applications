export default function createCardContent(Component) {
    return class CardContent extends Component {
        constructor(...decorators) {
            super('div');
            decorators.forEach(d => this.addDecorator(d));
        }
    };
}