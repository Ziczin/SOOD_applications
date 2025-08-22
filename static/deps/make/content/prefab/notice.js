export default function createNotice(core, Component) {
    class NoticeHandler {
        constructor() {
            this.noticeQueue = [];
            this.isNoticeActive = false;
        }

        add(notice, timeIn, timeStay, timeOut) {
            this.noticeQueue.push({ notice, timeIn, timeStay, timeOut });
            this.showNext();
        }

        async showNext() {
            if (this.isNoticeActive || this.noticeQueue.length === 0) return;
            this.isNoticeActive = true;

            const { notice, timeIn, timeStay, timeOut } = this.noticeQueue.shift();
            const el = notice.build();
            document.body.appendChild(el);

            await core.delay(50);
            el.style.transform = 'translateX(0)';

            await core.delay(timeIn + timeStay);

            el.style.transition = `transform ${timeOut}ms ease-in-out`;
            el.style.transform = 'translateX(100%)';

            await core.delay(timeOut);

            el.remove();
            this.isNoticeActive = false;
            this.showNext();
        }
    }

    class Notice extends Component {
        constructor(timeIn, timeStay, timeOut) {
            super('div');
            this.timeIn = timeIn;
            this.timeStay = timeStay;
            this.timeOut = timeOut;
        }
        
        build() {
            super.build();
            
            this.element.style.position = 'fixed';
            this.element.style.bottom = '1%';
            this.element.style.right = '0';
            this.element.style.transform = 'translateX(100%)';
            this.element.style.transition = `transform ${this.timeIn}ms ease-in-out`;
            this.element.style.zIndex = '1000';
            this.element.style.minWidth = '25%';
            this.element.style.maxWidth = '100%';
            
            return this.element;
        }
    }

    const noticeHandler = new NoticeHandler();

    return function createNotice (timeIn, timeStay, timeOut, ...decorators) {
        const notice = new Notice(timeIn, timeStay, timeOut);
        
        notice.addModifiers(...decorators);
        
        notice.build();
        noticeHandler.add(notice, timeIn, timeStay, timeOut);
        
        return notice;
    };
}