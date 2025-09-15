export default function createAnnotationFactory(core, Component) {
  class Annotation extends Component {
    constructor(delayMs = 800, ...modifiers) {
      super('div', false);
      this.name = 'annotation';
      this.delayMs = delayMs;
      this.addModifiers(...modifiers);
      this._showTimer = null;
      this._isShown = false;
      this._mousePos = { x: 0, y: 0 };
      this._domParent = null;
      this.elementPopup = null;
      this._observer = null;
      this._onParentEnter = this._onParentEnter.bind(this);
      this._onParentMove = this._onParentMove.bind(this);
      this._onParentLeave = this._onParentLeave.bind(this);
      this._onMutations = this._onMutations.bind(this);
    }

    build(force = false) {
      if (this.element && !force) return this.element;
      this.element = document.createElement(this.elementType);
      this.element.makeComponent = this;
      this.element.classList.add('make-annotation-placeholder');
      this.element.style.position = 'relative';
      this.element.style.minHeight = '0';
      this._tryAttachParent();
      return this.element;
    }

    _tryAttachParent() {
      const parentEl = this.element.parentNode;
      if (parentEl) {
        this._attachToParent(parentEl);
        return;
      }
      if (this._observer) return;
      this._observer = new MutationObserver(this._onMutations);
      this._observer.observe(document, { childList: true, subtree: true });
    }

    _onMutations() {
      if (!this.element) return;
      const parentEl = this.element.parentNode;
      if (parentEl) {
        this._attachToParent(parentEl);
        if (this._observer) {
          this._observer.disconnect();
          this._observer = null;
        }
      }
    }

    _attachToParent(parentEl) {
      if (this._domParent === parentEl) return;
      this._domParent = parentEl;
      parentEl.addEventListener('mouseenter', this._onParentEnter);
      parentEl.addEventListener('mousemove', this._onParentMove);
      parentEl.addEventListener('mouseleave', this._onParentLeave);
    }

    destroy() {
      if (this._domParent) {
        this._domParent.removeEventListener('mouseenter', this._onParentEnter);
        this._domParent.removeEventListener('mousemove', this._onParentMove);
        this._domParent.removeEventListener('mouseleave', this._onParentLeave);
        this._domParent = null;
      }
      if (this._observer) {
        this._observer.disconnect();
        this._observer = null;
      }
      this._clearShowTimer();
      this._hideImmediate();
      this.children = [];
      if (this.element && this.element.parentNode) this.element.parentNode.removeChild(this.element);
      this.element = null;
      this.destroyed = true;
    }

    _onParentEnter(ev) {
      this._updateMouse(ev);
      this._clearShowTimer();
      this._showTimer = setTimeout(() => this._show(ev), this.delayMs);
    }

    _onParentMove(ev) {
      this._updateMouse(ev);
      if (this._isShown) this._positionPopup();
    }

    _onParentLeave() {
      this._clearShowTimer();
      this._hide();
    }

    _updateMouse(ev) {
      this._mousePos.x = ev.clientX;
      this._mousePos.y = ev.clientY;
    }

    _clearShowTimer() {
      if (this._showTimer) {
        clearTimeout(this._showTimer);
        this._showTimer = null;
      }
    }

    buildPopup() {
      if (this.elementPopup) return this.elementPopup;
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
      this.elementPopup = popup;
      return popup;
    }

    async _show(ev) {
      if (this._isShown) return;
      if (this.children.length === 0) return;
      const popup = this.buildPopup();
      document.body.appendChild(popup);
      this._isShown = true;
      this._positionPopup();
      await core.delay(10);
      if (popup) popup.style.opacity = '1';
    }

    _positionPopup() {
      const popup = this.elementPopup;
      if (!popup) return;
      const padding = 8;
      const rect = popup.getBoundingClientRect();
      let left = this._mousePos.x + 12;
      let top = this._mousePos.y + 12;
      if (left + rect.width + padding > window.innerWidth) {
        left = this._mousePos.x - rect.width - 12;
        if (left < padding) left = padding;
      }
      if (top + rect.height + padding > window.innerHeight) {
        top = this._mousePos.y - rect.height - 12;
        if (top < padding) top = padding;
      }
      popup.style.left = `${Math.round(left)}px`;
      popup.style.top = `${Math.round(top)}px`;
    }

    async _hide() {
      if (!this._isShown || !this.elementPopup) return;
      this.elementPopup.style.opacity = '0';
      await core.delay(120);
      this._destroyPopup();
      this._isShown = false;
    }

    _hideImmediate() {
      if (this.elementPopup && this.elementPopup.parentNode) this.elementPopup.parentNode.removeChild(this.elementPopup);
      this.elementPopup = null;
      this._isShown = false;
    }

    _destroyPopup() {
      if (!this.elementPopup) return;
      if (this.elementPopup.parentNode) this.elementPopup.parentNode.removeChild(this.elementPopup);
      this.elementPopup = null;
    }
  }

  function AnnotationFactory(delayMs = 800, ...modifiers) {
    return new Annotation(delayMs, ...modifiers);
  }

  return AnnotationFactory;
}
