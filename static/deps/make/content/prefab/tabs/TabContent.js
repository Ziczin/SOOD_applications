export default function createTabContent(Component) {
    return class TabContent extends Component {
        constructor(...decorators) {
            super('div');
            decorators.forEach(d => this.addDecorator(d));
        }
    };
}