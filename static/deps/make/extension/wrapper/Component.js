import Applicable from '../mixin/Applicable.js';

export default class Component extends Applicable {
    constructor(elementType, autoRebuild = true) {
        super(); // Важно оставить super()
        this.elementType = elementType;
        this.element = null;
        this.decorators = [];
        this.children = [];
        this.parent = null;
        this.autoRebuild = autoRebuild;
    }

    addDecorator(decorator) {
        this.decorators.push(decorator);
        return this;
    }

    addChild(...items) {
        for (const item of items) {
            if (item instanceof Component) {
                item.parent = this;
                this.children.push(item);
            }
        }
        if (this.autoRebuild) {
            this.build(true);
        }
        return this;
    }

    build(force = false) {
        if (this.element) {
            if (force) this.element.innerHTML = '';
            else return this.element;
        }
        else this.element = document.createElement(this.elementType);
        
        for (const decorator of this.decorators) {
            decorator.apply(this);
        }

        for (const child of this.children) {
            this.element.appendChild(child.build());
        }

        return this.element;
    }

    apply(parent) {
        if (parent instanceof Component && !this.parent) {
            parent.addChild(this);
        }
    }
}

