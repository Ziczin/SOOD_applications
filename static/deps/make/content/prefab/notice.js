export default function createNoticeFactory(core, Component, Event, Preferences) {
    class NoticeHandler {
        constructor() {
            this.noticeQueue = [];
            this.activeNotice = null;
            this.activeIds = new Set();
            this.add = this.add.bind(this);
            this.showNext = this.showNext.bind(this);
            this.getActive = this.getActive.bind(this);
            this.closeActive = this.closeActive.bind(this);
            this.onAddNewNotice = new Event(this)
        }

        add(notice) {
            this.onAddNewNotice.emit()
            this.activeNotice?.onAddNewNotice.emit()
            let id = notice.pref.get('id')
            if (id) {
                if (this.activeIds.has(id) || this._queueHasId(id)) {
                    return false;
                }
                this.activeIds.add(id);
            }
            
            this.noticeQueue.push(notice);
            
            if (this.activeNotice && this.activeNotice.pref.get('weak')) {
                this.closeActive();
            } else {
                this.showNext();
            }
            return true;
        }

        _queueHasId(id) {
            return this.noticeQueue.some(n => n.pref.get('id') === id);
        }

        async showNext() {
            if (this.activeNotice && !this.activeNotice.pref.get('weak')) {
                return;
            }
            
            if (this.noticeQueue.length === 0) return;
            
            const notice = this.noticeQueue.shift();
            let id = notice.pref.get('id')

            const el = notice.build();
            document.body.appendChild(el);

            this.activeNotice = notice;

            try {
                if (!this.activeNotice.pref.get('weak') || this.noticeQueue.length === 0) {
                    await notice.open();
                    notice.startAutoCloseTimer();
                    await notice.closed;
                }
            } finally {
                this.activeNotice = null;
                if (id) {
                    this.activeIds.delete(id);
                }
                if (el && el.parentNode) {
                    el.remove();
                }
                this.showNext();
            }
        }

        getActive() {
            return this.activeNotice;
        }

        closeActive() {
            if (this.activeNotice && typeof this.activeNotice.close === 'function') {
                this.activeNotice.close();
                return true;
            }
            return false;
        }
    }

    class Notice extends Component {
        constructor(pref) {
            super('div');
            this.name = 'notice';
            this.pref = pref;
            this.pref.set('in', 500);
            this.pref.set('stay', 1500);
            this.pref.set('out', 500);
            this._autoCloseTimer = null;
            this._isOpen = false;
            this._isClosing = false;
            this.closed = new Promise(resolve => this._resolveClosed = resolve);
            this.onAddNewNotice = new Event(this)
        }

        build(force = false) {
            const el = super.build(force);
            if (el) {
                el.style.position = 'fixed';
                el.style.bottom = '1%';
                el.style.right = '0';
                el.style.transform = 'translateX(100%)';
                el.style.transition = `transform ${this.pref.get('in')}ms ease-in-out`;
                el.style.zIndex = '10000';
                el.style.display = 'flexbox';
                el.style.minWidth = '25%';
                el.style.maxWidth = '100%';
                el.style.minHeight = '0';
                el.style.maxHeight = '98vh';
            }
            return el;
        }

        async open() {
            if (this._isOpen || this._isClosing) return;
            if (!this.element) this.build();
            this.element.style.transition = `transform ${this.pref.get('in')}ms ease-in-out`;
            await core.delay(50);
            this.element.style.transform = 'translateX(0)';
            this._isOpen = true;
            await core.delay(this.pref.get('in'));
        }

        startAutoCloseTimer() {
            if (!isFinite(this.pref.get('stay')) || this.pref.get('stay') <= 0) return;
            this.cancelAutoClose();
            this._autoCloseTimer = setTimeout(() => this.close(), this.pref.get('stay'));
        }

        cancelAutoClose() {
            if (this._autoCloseTimer) {
                clearTimeout(this._autoCloseTimer);
                this._autoCloseTimer = null;
            }
        }

        async close() {
            if (!this._isOpen || this._isClosing) return;
            this._isClosing = true;
            this.cancelAutoClose();
            if (!this.element) {
                this._resolveClosed();
                return;
            }
            this.element.style.transition = `transform ${this.pref.get('out')}ms ease-in-out`;
            this.element.style.transform = 'translateX(100%)';
            await core.delay(this.pref.get('out'));
            this._resolveClosed();
            this.destroy()
        }
    }

    const noticeHandler = new NoticeHandler();

    function createNotice(pref, ...decorators) {
        if (!(pref instanceof Preferences)) {
            pref = new Preferences(...pref);
        }
        pref.parse("in stay out id")
        const notice = new Notice(pref);
        notice.addModifiers(...decorators);
        noticeHandler.add(notice);
        return notice;
    }

    return {
        createNotice,
        noticeHandler
    };
}