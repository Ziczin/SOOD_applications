export default function createAnnotationFactory(core, Component) {
  class Annotation extends Component {
    constructor(delayMs = 800, ...modifiers) {
      super('div', false);
      this.name = 'annotation';
      this.delayMs = delayMs;
      this.addModifiers(...modifiers);
      this.showTimer = null;
      this.mousePos = { x: 0, y: 0 };
      this.element = null;
      this.onParentEnter = this.onParentEnter.bind(this);
      this.onParentMove = this.onParentMove.bind(this);
      this.onParentLeave = this.onParentLeave.bind(this);
    }

    build(force = false) {
      if (this.element && !force) return this.element;
      this.parent?.allowEvents()
      this.element = document.createElement(this.elementType);
      this.element.makeComponent = this;
      this.element.classList.add('make-annotation-placeholder');
      this.element.style.position = 'relative';
      this.element.style.minHeight = '0';
      const parentEl = this.parent && this.parent.element;
      if (parentEl) {
        this.attachToParent(parentEl);
      }
      return this.element;
    }

    attachToParent(parentEl) {
      if (!parentEl) return;
      this.parent.element.addEventListener('mouseenter', this.onParentEnter);
      this.parent.element.addEventListener('mousemove', this.onParentMove);
      this.parent.element.addEventListener('mouseleave', this.onParentLeave);
    }

    destroy() {
      if (this.parent && this.parent.element) {
        this.parent.element.removeEventListener('mouseenter', this.onParentEnter);
        this.parent.element.removeEventListener('mousemove', this.onParentMove);
        this.parent.element.removeEventListener('mouseleave', this.onParentLeave);
      }
      this.clearShowTimer();
      this.hideImmediate();
      this.children = [];
      if (this.element && this.element.parentNode) this.element.parentNode.removeChild(this.element);
      this.element = null;
      this.destroyed = true;
    }

    onParentEnter(ev) {
      this.updateMouse(ev);
      this.clearShowTimer();
      this.showTimer = setTimeout(() => this.show(ev), this.delayMs);
    }

    onParentMove(ev) {
      this.updateMouse(ev);
      this.positionPopup();
    }

    onParentLeave() {
      this.clearShowTimer();
      this.hide();
    }

    updateMouse(ev) {
      this.mousePos.x = ev.clientX;
      this.mousePos.y = ev.clientY;
    }

    clearShowTimer() {
      if (this.showTimer) {
        clearTimeout(this.showTimer);
        this.showTimer = null;
      }
    }

    buildPopup() {
      const popup = document.createElement('div');
      popup.classList.add('make-annotation-popup');
      popup.style.position = 'fixed';
      popup.style.pointerEvents = 'none';
      popup.style.opacity = '0';
      popup.style.transition = 'opacity 200ms ease';
      popup.style.zIndex = '4000';
      for (const child of this.children) {
        if (!child.destroyed) popup.appendChild(child.build(true));
      }
      this.element = popup;
      return popup;
    }

    async show(ev) {
      document.querySelectorAll('.make-annotation-popup').forEach(function(el){
        el.remove();
      });
      const popup = this.buildPopup();
      document.body.appendChild(popup);
      this.positionPopup();
      await core.delay(10);
      if (popup) popup.style.opacity = '1';
      if (!(this.parent?.element?.display !== 'none'))
        this.hide()
    }

    positionPopup() {
      const popup = this.element;
      if (!popup) return;
      const padding = 8;
      const rect = popup.getBoundingClientRect();
      let left = this.mousePos.x + 12;
      let top = this.mousePos.y + 12;
      if (left + rect.width + padding > window.innerWidth) {
        left = this.mousePos.x - rect.width - 12;
        if (left < padding) left = padding;
      }
      if (top + rect.height + padding > window.innerHeight) {
        top = this.mousePos.y - rect.height - 12;
        if (top < padding) top = padding;
      }
      popup.style.left = `${Math.round(left)}px`;
      popup.style.top = `${Math.round(top)}px`;
    }

    async hide() {
      if (!this.element) return;
      this.element.style.opacity = '0';
      await core.delay(120);
      this.destroyPopup();
    }

    hideImmediate() {
      if (this.element && this.element.parentNode) this.element.parentNode.removeChild(this.element);
      this.element = null;
    }

    destroyPopup() {
      if (!this.element) return;
      if (this.element.parentNode) this.element.parentNode.removeChild(this.element);
      this.element = null;
    }
  }

  const annotationsArray = []

  function AnnotationFactory(delayMs = 800, ...modifiers) {
    return new Annotation(delayMs, ...modifiers)
  }

  return AnnotationFactory;
}
