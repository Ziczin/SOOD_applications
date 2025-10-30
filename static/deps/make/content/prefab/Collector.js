export default (Component) => class Collector extends Component {
    constructor(...modifiers) {
        super('form', true);
        this.name = 'collector';
        this.records = [];
        this._listeners = new WeakMap();
        this.addModifiers(...modifiers)
    }

    _recordFromElement(el) {
        const tag = el.tagName ? el.tagName.toLowerCase() : null;
        const value = (el.value !== undefined) ? el.value : null;
        const rec = { tag, value };
        if (el.name) rec.name = el.name;
        if (el.id) rec.id = el.id;
        return rec;
    }

    _findRecordIndexForElement(el) {
        if (el.name) {
            const idx = this.records.findIndex(r => r.name === el.name);
            if (idx !== -1) return idx;
        }
        if (el.id) {
            const idx = this.records.findIndex(r => r.id === el.id);
            if (idx !== -1) return idx;
        }
        const idxByEl = this.records.findIndex(r => r._el === el);
        return idxByEl;
    }

    _upsertElementRecord(el) {
        const rec = this._recordFromElement(el);
        const idx = this._findRecordIndexForElement(el);
        if (idx !== -1) {
            const existing = this.records[idx];
            this.records[idx] = Object.assign({}, existing, rec);
            this.records[idx]._el = el;
        } else {
            const toStore = Object.assign({}, rec, { _el: el });
            this.records.push(toStore);
        }
    }

    _attachListener(el) {
        if (!el || !(el instanceof Element)) return;
        const tag = el.tagName ? el.tagName.toLowerCase() : '';
        if (tag !== 'input' && tag !== 'select' && tag !== 'textarea') return;
        if (this._listeners.has(el)) return;
        const handler = () => {
            this._upsertElementRecord(el);
        };
        const events = [];
        if (tag === 'select') events.push('change'); else events.push('input');
        if (tag === 'input') {
            const t = (el.type || '').toLowerCase();
            if (t === 'checkbox' || t === 'radio') {
                events.splice(0, events.length, 'change');
            }
        }
        for (const ev of events) {
            el.addEventListener(ev, handler);
        }
        this._listeners.set(el, { handler, events });
    }

    _detachListener(el) {
        const info = this._listeners.get(el);
        if (!info) return;
        for (const ev of info.events) {
            el.removeEventListener(ev, info.handler);
        }
        this._listeners.delete(el);
    }

    _collectFromComponentTree(comp) {
        if (comp.element) {
            const nodes = comp.element.querySelectorAll('input, select, textarea');
            nodes.forEach(el => {
                this._upsertElementRecord(el);
                this._attachListener(el);
            });
        }
        for (const child of comp.children) {
            this._collectFromComponentTree(child);
        }
    }

    collect() {
        this._collectFromComponentTree(this);
        this.records = this.records.filter(r => {
            if (!r._el) return true;
            return document.contains(r._el);
        });
        return this.records.map(r => {
            const copy = Object.assign({}, r);
            delete copy._el;
            return copy;
        });
    }

    build(force = false) {
        const el = super.build(force);
        this.collect();
        return el;
    }

    addChild(child) {
        const res = super.addChild(child);
        this._attachToChildRecursively(child);
        return res;
    }

    removeChild(child) {
        const res = super.removeChild(child);
        this._detachFromChildRecursively(child);
        this.collect();
        return res;
    }

    _attachToChildRecursively(comp) {
        if (comp.element) {
            const nodes = comp.element.querySelectorAll('input, select, textarea');
            nodes.forEach(el => {
                this._upsertElementRecord(el);
                this._attachListener(el);
            });
        }
        for (const c of comp.children) {
            this._attachToChildRecursively(c);
        }
    }

    _detachFromChildRecursively(comp) {
        if (comp.element) {
            const nodes = comp.element.querySelectorAll('input, select, textarea');
            nodes.forEach(el => {
                this._detachListener(el);
                const idx = this.records.findIndex(r => r._el === el);
                if (idx !== -1) this.records.splice(idx, 1);
            });
        }
        for (const c of comp.children) {
            this._detachFromChildRecursively(c);
        }
    }

    destroy() {
        if (this._listeners.keys)
            for (const key of this._listeners.keys())
                this._detachListener(key);
        this._listeners = new WeakMap();
        this.records = [];
        super.destroy();
    }
}
