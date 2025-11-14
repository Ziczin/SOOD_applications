export default (Component) =>
class Modal extends Component {
    constructor({
        left = '20vw',
        top = '20vh',
        width = '60vw',
        height = '60vh',
        fadeIn = 300,
        fadeOut = 300,
        elementType = 'div',
        autoRebuild = true,
        blur = 0,
        autoHeight = false
    } = {}, ...modifiers) {
        super(elementType, autoRebuild)
        this.name = 'overlayComponent'
        this.left = left
        this.top = top
        this.width = width
        this.height = height
        this.fadeIn = fadeIn
        this.fadeOut = fadeOut
        this.blur = blur
        this.autoHeight = autoHeight
        this.buildLock = false
        this.blurElement = null
        this._removeTimers = new Set()
        this._boundResize = this._onWindowResize.bind(this)
        this.addModifiers(...modifiers)
    }
    
    allowEvents() {
        super.allowEvents()
        if (!this.onOpenStart) this.onOpenStart = new Event({ret: this})
        if (!this.onOpenEnd) this.onOpenEnd = new Event({ret: this})
        if (!this.onCloseStart) this.onCloseStart = new Event({ret: this})
        if (!this.onCloseEnd) this.onCloseEnd = new Event({ret: this})
        return this
    }

    createBlurElement() {
        if (this.blurElement) return this.blurElement
        if (!this.blur || this.blur <= 0) return null
        const be = document.createElement('div')
        Object.assign(be.style, {
            position: 'fixed',
            left: '0',
            top: '0',
            width: '100vw',
            height: '100vh',
            zIndex: '999',
            pointerEvents: 'auto',
            backdropFilter: `blur(${this.blur}px)`,
            WebkitBackdropFilter: `blur(${this.blur}px)`,
            transition: `opacity ${this.fadeIn}ms ease`,
            opacity: '0',
            background: 'transparent',
            boxSizing: 'border-box'
        })
        this.blurElement = be
        return be
    }

    _applyAutoHeight() {
        if (!this.element) return
        if (!this.autoHeight) {
            this.element.style.height = this.height
            this.element.style.maxHeight = '60vw'
            this.element.style.overflow = 'auto'
            return
        }
        this.element.style.height = 'auto'
        this.element.style.maxHeight = this.height
        this.element.style.overflow = 'auto'
    }

    _onWindowResize() {
        this._applyAutoHeight()
    }

    _safeCallEvent(eventObj, payload) {
        if (!eventObj) return
        if (typeof eventObj.emit === 'function') {
            eventObj.emit(payload)
            return
        }
        if (typeof eventObj.trigger === 'function') {
            eventObj.trigger(payload)
            return
        }
        if (typeof eventObj === 'function') {
            eventObj(payload)
            return
        }
    }

    build(force = false) {
        const el = super.build(force)

        Object.assign(el.style, {
            position: 'fixed',
            left: this.left,
            top: this.top,
            width: this.width,
            zIndex: '1000',
            boxSizing: 'border-box',
            opacity: '0',
            transition: `opacity ${this.fadeIn}ms ease`,
            pointerEvents: 'auto',
            overflow: 'visible',
            border: '1px solid transparent',
            maxHeight: 'fit-content',
            minHeight: '0'
        })

        if (this.autoHeight) {
            this._applyAutoHeight()
        } else {
            el.style.height = this.height
        }

        if (!el.parentNode) {
            if (this.blur && this.blur > 0) {
                const be = this.createBlurElement()
                if (be && !be.parentNode) document.body.appendChild(be)
            }
            document.body.appendChild(el)
        }
        
        if (this.blurElement) {
            requestAnimationFrame(() => {
                this.blurElement && (this.blurElement.style.opacity = '1')
            })
        }

        this._safeCallEvent(this.onOpenStart, this)
        requestAnimationFrame(() => {
            el.offsetHeight
            el.style.opacity = '1'
        })
        this._safeCallEvent(this.onOpenEnd, this)

        if (this.autoHeight) {
            window.addEventListener('resize', this._boundResize)
            const originalOnBuild = this.onBuild
            if (originalOnBuild) {
                const self = this
                this.onBuild = {
                    emit(...args) {
                        if (originalOnBuild && typeof originalOnBuild.emit === 'function') originalOnBuild.emit.apply(originalOnBuild, args)
                        self._applyAutoHeight()
                    },
                    trigger(...args) {
                        if (originalOnBuild && typeof originalOnBuild.trigger === 'function') originalOnBuild.trigger.apply(originalOnBuild, args)
                        self._applyAutoHeight()
                    }
                }
            }
        }

        return el
    }

    _clearAllTimers() {
        for (const id of this._removeTimers) {
            clearTimeout(id)
        }
        this._removeTimers.clear()
    }

    close() {
        if (!this.element && !this.blurElement) return
        const el = this.element

        if (el) {
            el.style.transition = `opacity ${this.fadeOut}ms ease`
            el.style.opacity = '0'
        }

        if (this.blurElement) {
            this.blurElement.style.transition = `opacity ${this.fadeOut}ms ease`
            this.blurElement.style.opacity = '0'
        }

        const removeAfter = this.fadeOut

        this._safeCallEvent(this.onCloseStart, this)
        const id = setTimeout(() => {
            if (el && el.parentNode) el.parentNode.removeChild(el)
            if (this.blurElement && this.blurElement.parentNode) {
                this.blurElement.parentNode.removeChild(this.blurElement)
            }
            this._removeTimers.delete(id)
            this.blurElement = null
            this.destroy()
        }, removeAfter)
        this._removeTimers.add(id)
        this._safeCallEvent(this.onCloseEnd, this)

    }

    destroy() {
        this._clearAllTimers()
        window.removeEventListener('resize', this._boundResize)
        super.destroy()
        if (this.blurElement && this.blurElement.parentNode) {
            this.blurElement.parentNode.removeChild(this.blurElement)
        }
        this.blurElement = null
    }
}
