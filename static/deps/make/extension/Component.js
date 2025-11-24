const dataTestIds = {}

function getRelatedTestId(name) {
  if (!dataTestIds[name]) {
    dataTestIds[name] = 0
  }
  dataTestIds[name] += 1
  const id = dataTestIds[name]
  return `make-${name}-${id}`
}

export default (Decorator, Event, generateTestIds) =>
class Component {
    constructor(elementType, autoRebuild = true) {
        this.elementType = elementType;
        this.element = null;
        this.parent = null;
        this.decorators = [];
        this.children = [];
        this.buildLock = true
        this.destroyed = false;
        this.doEvents = false
        this.autoRebuild = autoRebuild;
    }

    getTestId() {
        if (this.testId) return this.testId
        if (generateTestIds) return getRelatedTestId(
            this.name || 'basic' + '-' + this.elementType
        )
    }

    allowEvents() {
        if (!this.doEvents) {
            this.doEvents = true
            this.onBuild = new Event({ret: this})
            this.onDestroy = new Event({ret: this})
            this.onChildAdd = new Event({ret: this})
            this.onChildDetach = new Event({ret: this})
            this.onChildRemove = new Event({ret: this})
            this.onSwap = new Event({ret: this})
        }
        return this
    }

    pushModifiers(...modifiers) {
        for (const modifier of modifiers) {
            modifier instanceof Component && this.pushChild(modifier);   
            modifier instanceof Decorator && this.addDecorator(modifier);
            modifier instanceof Function && this.addDecorator(modifier)
        }
    }

    addModifiers(...modifiers) {
        const autoRebuild = this.autoRebuild
        this.autoRebuild = false
        for (const modifier of modifiers) {
            modifier instanceof Component && this.addChild(modifier);   
            modifier instanceof Decorator && this.addDecorator(modifier);
            modifier instanceof Function && this.addDecorator(modifier)
        }
        this.autoRebuild = autoRebuild
        if (this.element && this.autoRebuild) this.build(true);
        return this
    }

    addDecorator(decorator) {
        this.decorators.push(decorator)
    }

    pushChild(child) {
        child.parent = this;
        this.children.push(child);
    }

    addChild(child) {
        this.pushChild(child);
        if (this.autoRebuild) this.build(true);
        this.onChildAdd?.emit(child)
    }

    build(force = false) {
        if (this.element) {
            if (force) this.element.innerHTML = '';
            else return this.element;
        }
        else {
            this.element = document.createElement(this.elementType);
            if (generateTestIds) this.element.setAttribute('data-test-id', this.getTestId())
            this.element.makeComponent = this
        }
        this.decorators.forEach((decorator) => decorator.apply(this))
        this.children.forEach((child) => {
            this.element.appendChild(child.build())
        })
        this.onBuild?.emit(this)
        return this.element;
    }

    destroy(detach = true) {
        if (this.destroyed) return;
        this.destroyed = true;
        
        if (this.parent && detach) this.parent.detachChild(this)

        this.children.forEach(child => child.destroy(false));
        this.children = [];
        this.decorators = [];
        
        this.element = null;

        if (this.doEvents) {
            this.doEvents = null
            this.onBuild = null
            this.onDestroy = null
            this.onChildAdd = null
            this.onChildDetach = null
            this.onChildRemove = null
            this.onSwap = null
        }

        this.destroyed = null;

        this.onDestroy?.emit(this)
    }

    detachChild(child) {
        const index = this.children.indexOf(child);
        if (index !== -1){
            this.children.splice(index, 1);
            child.parent = null;
        }
        if (this.autoRebuild && this.element) {
            this.build(true);
        }
        this.onChildDetach?.emit(child)
        return this
    }

    removeChild(child) {
        this.detachChild(child)
        child.destroy()
        this.onChildRemove?.emit(child)
        return this;
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
        return this
    }
}
