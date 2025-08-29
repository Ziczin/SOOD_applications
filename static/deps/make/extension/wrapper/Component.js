import Applicable from '../mixin/Applicable.js';
import Decorator from './Decorator.js';

export default class Component extends Applicable {
    constructor(elementType, autoRebuild = true) {
        super();
        this.name = 'component'
        this.elementType = elementType;
        this.element = null;
        this.decorators = [];
        this.children = [];
        this.parent = null;
        this.autoRebuild = autoRebuild;
        this.buildLock = true
        this.destroyed = false;
    }

    view() {
        return `${this.elementType}=${this.name}`
    }

    addModifiers(...modifiers) {
        for (const modifier of modifiers) {
            modifier instanceof Component && this.addChild(modifier);   
            modifier instanceof Decorator && this.addDecorator(modifier);
            modifier instanceof Function && this.addDecorator(modifier)
        }
        return this
    }

    addDecorator(decorator) {
        this.decorators.push(decorator)
    }

    addChild(child) {
        //console.log(`${this.view()} <- ${child.view()}`)
        child.parent = this;
        this.children.push(child);
        this.autoRebuild && this.build(true);
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
            if (!child.destroyed) {
                this.element.appendChild(child.build());
            }
        }
        return this.element;
    }

    destroy() {
        if (this.destroyed) return;
        this.destroyed = true;
        
        if (this.parent) {
            this.parent.removeChild(this);
            this.parent = null;
        }
        this.decorators = [];
        
        this.children.forEach(child => child.destroy());
        this.children = [];
        
        if (this.element && this.element.parentNode) {
            this.element.parentNode.removeChild(this.element);
        }
        this.element = null;
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
}