import Applicable from '../mixin/Applicable.js';

export default class Component extends Applicable {
    constructor(elementType, autoRebuild = true) {
        super();
        this.elementType = elementType;
        this.element = null;
        this.decorators = [];
        this.children = [];
        this.parent = null;
        this.autoRebuild = autoRebuild;
        this.destroyed = false;
    }

    getChild(index) {
        return this.children[index] || null;
    }

    getFirstChild() {
        return this.children[0] || null;
    }

    getLastChild() {
        return this.children[this.children.length - 1] || null;
    }

    removeChild(child) {
        const index = this.children.indexOf(child);
        if (index === -1) return false;
        
        this.children.splice(index, 1);
        
        if (this.autoRebuild && this.element) {
            this.build(true);
        }
        
        return true;
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
        if (this.destroyed) {
            return null;
        }
        
        if (this.element) {
            if (force) this.element.innerHTML = '';
            else return this.element;
        }
        else this.element = document.createElement(this.elementType);
        
        for (const decorator of this.decorators) {
            try {
                decorator.apply(this);
            }
            catch (e) {
                console.log(this)
                console.log(e)
                console.log(decorator)
            }
        }

        for (const child of this.children) {
            if (!child.destroyed) {
                this.element.appendChild(child.build());
            }
        }

        return this.element;
    }

    apply(parent) {
        if (parent instanceof Component && !this.parent) {
            parent.addChild(this);
        }
    }

    destroy() {
        if (this.destroyed) return;
        this.destroyed = true;
        
        try {
            if (this.parent) {
                this.parent.removeChild(this);
            }
            
            this.decorators.forEach(decorator => {
                if (decorator.cleanup) decorator.cleanup(this);
            });
            
            [...this.children].forEach(child => child.destroy());
            
            if (this.element && this.element.parentNode) {
                this.element.parentNode.removeChild(this.element);
            }
        } finally {
            this.element = null;
            this.decorators = [];
            this.children = [];
            this.parent = null;
        }
    }
}