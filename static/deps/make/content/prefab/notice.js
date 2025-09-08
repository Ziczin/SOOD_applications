export default function createNoticeFactory(core, Component) {
    class NoticeHandler {
        constructor() {
            this.noticeQueue = [];
            this.isNoticeActive = false;
            this.activeNotice = null;
            this.activeIds = new Set();
            this.add = this.add.bind(this);
            this.showNext = this.showNext.bind(this);
            this.getActive = this.getActive.bind(this);
            this.closeActive = this.closeActive.bind(this);
        }

        add(notice) {
            if (notice.id) {
                if (this.activeIds.has(notice.id) || this._queueHasId(notice.id)) {
                    return false;
                }
            }
            this.noticeQueue.push(notice);
            this.showNext();
            return true;
        }

        _queueHasId(id) {
            return this.noticeQueue.some(n => n.id === id);
        }

        async showNext() {
            if (this.isNoticeActive || this.noticeQueue.length === 0) return;
            this.isNoticeActive = true;

            const notice = this.noticeQueue.shift();

            if (notice.id) this.activeIds.add(notice.id);

            const el = notice.build();
            document.body.appendChild(el);

            this.activeNotice = notice;

            try {
                await notice.open();
                notice.startAutoCloseTimer();
                await notice.closed;
            } finally {
                this.activeNotice = null;
                if (notice.id) this.activeIds.delete(notice.id);
                if (el && el.parentNode) el.remove();
                this.isNoticeActive = false;
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
        constructor(timeIn = 300, timeStay = 3000, timeOut = 300) {
            super('div');
            this.name = 'notice';
            this.timeIn = timeIn;
            this.timeStay = timeStay;
            this.timeOut = timeOut;
            this.id = null;
            this._autoCloseTimer = null;
            this._isOpen = false;
            this._isClosing = false;
            this.closed = new Promise(resolve => this._resolveClosed = resolve);
        }

        build(force = false) {
            const el = super.build(force);
            if (el) {
                el.style.position = 'fixed';
                el.style.bottom = '1%';
                el.style.right = '0';
                el.style.transform = 'translateX(100%)';
                el.style.transition = `transform ${this.timeIn}ms ease-in-out`;
                el.style.zIndex = '1000';
                el.style.minWidth = '25%';
                el.style.maxWidth = '100%';
            }
            return el;
        }

        async open() {
            if (this._isOpen || this._isClosing) return;
            if (!this.element) this.build();
            this.element.style.transition = `transform ${this.timeIn}ms ease-in-out`;
            await core.delay(50);
            this.element.style.transform = 'translateX(0)';
            this._isOpen = true;
            await core.delay(this.timeIn);
        }

        startAutoCloseTimer() {
            if (!isFinite(this.timeStay) || this.timeStay <= 0) return;
            this.cancelAutoClose();
            this._autoCloseTimer = setTimeout(() => this.close(), this.timeStay);
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
            this.element.style.transition = `transform ${this.timeOut}ms ease-in-out`;
            this.element.style.transform = 'translateX(100%)';
            await core.delay(this.timeOut);
            this._resolveClosed();
        }
    }

    const noticeHandler = new NoticeHandler();

    function createNotice(timeIn = 300, timeStay = 3000, timeOut = 300, ...decorators) {
        const notice = new Notice(timeIn, timeStay, timeOut);
        notice.addModifiers(...decorators);
        noticeHandler.add(notice);
        return notice;
    }

    function createUniqueNotice(id, timeIn = 300, timeStay = 3000, timeOut = 300, ...decorators) {
        const notice = new Notice(timeIn, timeStay, timeOut);
        notice.id = id;
        notice.addModifiers(...decorators);
        noticeHandler.add(notice);
        return notice;
    }

    return {
        createNotice,
        createUniqueNotice,
        noticeHandler
    };
}
