export default (Decorator, Event) => 
class Component {
    constructor(elementType, autoRebuild = true) {
        this.name = 'component'
        this.elementType = elementType;
        this.element = null;
        this.decorators = [];
        this.children = [];
        this.parent = null;
        this.autoRebuild = autoRebuild;
        this.buildLock = true
        this.destroyed = false;
        this.doEvents = false
    }

    allowEvents() {
        if (!this.doEvents) {
            this.doEvents = true
            this.onBuild = new Event({ret: this})
            this.onDestroy = new Event({ret: this})
            this.onChildAdd = new Event({ret: this})
            this.onChildRemove = new Event({ret: this})
            this.onSwap = new Event({ret: this})
        }
        return this
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
        child.parent = this;
        this.children.push(child);
        this.autoRebuild && this.build(true);
        this.onChildAdd?.emit(child)
    }

    build(force = false) {
        if (this.element) {
            if (force) this.element.innerHTML = '';
            else return this.element;
        }
        else this.element = document.createElement(this.elementType);
        this.element.makeComponent = this
        for (const decorator of this.decorators) {
            decorator.apply(this);
        }

        for (const child of this.children) {
            if (!child.destroyed) {
                this.element.appendChild(child.build());
            }
        }
        this.onBuild?.emit(this)
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
        this.onDestroy?.emit(this)
    }

    removeChild(child, destroy=true) {
        const index = this.children.indexOf(child);
        if (index === -1) return false;
        this.children.splice(index, 1);
        if (destroy) child.destroy()
        if (this.autoRebuild && this.element) {
            this.build(true);
        }
        this.onChildRemove?.emit(child)
        return true;
    }

    swap(other) {
        const a = this;
        const b = other;
        const aParent = a.parent;
        const bParent = b.parent;
        const aIndex = aParent.children.indexOf(a);
        const bIndex = bParent.children.indexOf(b);

        aParent.children[aIndex] = b;
        bParent.children[bIndex] = a;
        a.parent = bParent;
        b.parent = aParent;
        
        if (aParent.element && aParent.autoRebuild) aParent.build(true);
        if (bParent.element && bParent.autoRebuild) bParent.build(true);

        this.onSwap?.emit({ a, b });
    }
}
