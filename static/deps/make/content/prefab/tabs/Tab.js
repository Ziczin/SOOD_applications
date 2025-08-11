export default function createTab(Component, makeWith) {
    return class Tab extends Component {
        constructor(title, tabContent, ...decorators) {
            super('button');
            if (!tabContent || !(tabContent.constructor.name === 'TabContent')) {
                throw new Error('Tab requires exactly one TabContent element');
            }
            
            this.title = title;
            this.tabContent = tabContent;
            this.addDecorator(makeWith.text(title));
            this.addDecorator(makeWith.attr({ type: 'button' }));
            decorators.forEach(d => this.addDecorator(d));
        }
    };
}