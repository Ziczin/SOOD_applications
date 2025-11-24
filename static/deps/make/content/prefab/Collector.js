class Debouncer {
    constructor() {
        this.timers = new Map();
    }
    
    debounce(key, callback, delay) {
        this.cancel(key);
        const timerId = setTimeout(() => {
            callback();
            this.timers.delete(key);
        }, delay);
        this.timers.set(key, timerId);
    }
    
    cancel(key) {
        const timerId = this.timers.get(key);
        if (timerId) {
            clearTimeout(timerId);
            this.timers.delete(key);
        }
    }
    
    clear() {
        for (const timerId of this.timers.values()) {
            clearTimeout(timerId);
        }
        this.timers.clear();
    }
}

class EventListenerManager {
    constructor() {
        this.listeners = new WeakMap();
    }
    
    add(element, events, handler) {
        if (this.listeners.has(element)) return false;
        
        events.forEach(event => element.addEventListener(event, handler));
        this.listeners.set(element, { handler, events });
        return true;
    }
    
    remove(element) {
        const info = this.listeners.get(element);
        if (!info) return false;
        
        info.events.forEach(event => element.removeEventListener(event, info.handler));
        this.listeners.delete(element);
        return true;
    }
    
    clear() {
        if (this.listeners.keys) {
            for (const key of this.listeners.keys()) {
                this.remove(key);
            }
        }
    }
    
    has(element) {
        return this.listeners.has(element);
    }
}

class FieldValidator {
    static isElementRequired(element) {
        if (element.type?.toLowerCase() === 'checkbox') return false;
        return !!element.makeDataRequired;
    }
    
    static recordHasValue(record) {
        const element = record.element;
        if (element.type?.toLowerCase() === 'checkbox') return element.checked;
        if (element.type?.toLowerCase() === 'radio') {
            const group = document.querySelectorAll(`input[type="radio"][name="${element.name}"]`);
            return Array.from(group).some(item => item.checked);
        }
        return !!element.value;
    }
    
    static getElementEvents(element) {
        const tag = element.tagName.toLowerCase();
        const type = element.type?.toLowerCase() || '';
        const events = [];
        
        if (tag === 'select') {
            events.push('change');
        } else if (tag === 'input') {
            const changeTypes = ['checkbox', 'radio', 'time', 'date', 'datetime-local', 'month', 'week', 'range', 'file'];
            if (changeTypes.includes(type)) {
                events.push('change');
            } else {
                events.push('input');
                events.push('blur');
            }
        } else if (tag === 'textarea') {
            events.push('input');
            events.push('blur');
        }
        
        return events;
    }
    
    static needsDebounce(element) {
        const tag = element.tagName.toLowerCase();
        const elementType = element.type?.toLowerCase() || '';
        
        const debounceTypes = ['text', 'email', 'password', 'search', 'tel', 'url', 'number'];
        
        if (tag === 'textarea') return true;
        if (tag === 'input' && debounceTypes.includes(elementType)) return true;
        
        return false;
    }
}

export default (Component, Event) =>
class Collector extends Component {
    constructor(...modifiers) {
        super('form', true);
        this.name = 'collector';
        this.records = [];
        this.allRequiredFieldsFilled = null;
        this.debugAutoLog = false;
        
        this.debouncer = new Debouncer();
        this.listenerManager = new EventListenerManager();
        this.requiredListenerManager = new EventListenerManager();
        
        this.debounceTimeout = 200;
        this.initDebounceTimeout = 200;
        this.initTimer = null;
        this.collecting = false;
        
        this.pushModifiers(...modifiers);
    }

    emitRequiredEvents(newState) {
        this.allRequiredFieldsFilled = newState;

        if (this.doEvents) {
            if (newState) {
                this.onAllRequiredFieldsFilled?.emit();
            } else {
                this.onRequiredFieldMissing?.emit();
            }
        }

        this.checkDebugList();
    }

    build(force = false) {
        const element = super.build(force);
        
        this.collecting = true;
        this.collectFromComponentTree(this);
        const newState = this.computeAllRequiredFieldsFilled();
        this.emitRequiredEvents(newState);
        this.collecting = false;
        
        return element;
    }

    allowDebug(doDebug = true) {
        this.debugAutoLog = doDebug;
        return this;
    }

    allowEvents() {
        super.allowEvents();
        if (!this.onAllRequiredFieldsFilled) this.onAllRequiredFieldsFilled = new Event({ret: this});
        if (!this.onRequiredFieldMissing) this.onRequiredFieldMissing = new Event({ret: this});
        return this;
    }

    setDebounceTimeout(ms) {
        this.debounceTimeout = ms;
        return this;
    }

    setInitDebounceTimeout(ms) {
        this.initDebounceTimeout = ms;
        return this;
    }

    getFormElements(component) {
        if (!component.element) return [];
        return Array.from(component.element.querySelectorAll('input, select, textarea'));
    }

    processFormElements(component) {
        this.getFormElements(component).forEach(element => {
            this.upsertElementRecord(element);
            this.attachListener(element);
            this.attachRequiredListener(element);
        });
    }

    processChildrenRecursively(component, method) {
        component.children.forEach(child => method.call(this, child));
    }

    collect() {
        this.collectFromComponentTree(this);
        this.cleanupRecords();
        return this.getRecordsWithoutElements();
    }

    check() {
        this.collectFromComponentTree(this);
        this.cleanupRecords();
        return this.computeAllRequiredFieldsFilled();
    }

    checkDebugList() {
        if (!this.debugAutoLog) return;
        
        this.cleanupRecords();
        
        const list = [];
        const hasTestId = this.records.some(record => record.element.getAttribute('data-test-id'));
        const hasName = this.records.some(record => record.name);
        
        this.records.forEach(record => {
            const element = record.element;
            const makeReq = FieldValidator.isElementRequired(element);
            const isFilled = makeReq ? FieldValidator.recordHasValue(record) : true;
            
            let value;
            if (element.type?.toLowerCase() === 'checkbox') {
                value = element.checked;
            } else if (element.type?.toLowerCase() === 'radio') {
                const group = document.querySelectorAll(`input[type="radio"][name="${element.name}"]`);
                value = Array.from(group).some(item => item.checked);
            } else {
                value = element.value;
            }
            
            const tableRecord = { 
                ...(hasName && { name: record.name || null }),
                tag: record.tag || null, 
                makeDataRequired: makeReq, 
                value: value,
                isFilled: isFilled
            };
            
            if (hasTestId) {
                tableRecord['data-test-id'] = element.getAttribute('data-test-id') || null;
            }
            
            list.push(tableRecord);
        });
        
        const tableObject = {};
        list.forEach((item, index) => {
            tableObject[index + 1] = item;
        });
        console.table(tableObject);
        
        const currentState = this.computeAllRequiredFieldsFilled();
        console.log(`%cOverall required fields filled: ${currentState}`, 
            `color: ${currentState ? 'green' : 'red'}; font-weight: bold; font-size: 14px;`);
    }

    recordFromElement(element) {
        return {
            tag: element.tagName.toLowerCase(),
            value: element.value !== undefined ? element.value : null,
            name: element.name || null,
            id: element.id || null,
            makeDataRequired: !!element.makeDataRequired
        };
    }

    findRecordIndexForElement(element) {
        if (element.name) {
            const index = this.records.findIndex(record => record.name === element.name);
            if (index !== -1) return index;
        }
        if (element.id) {
            const index = this.records.findIndex(record => record.id === element.id);
            if (index !== -1) return index;
        }
        return this.records.findIndex(record => record.element === element);
    }

    upsertElementRecord(element) {
        const newRecord = this.recordFromElement(element);
        const index = this.findRecordIndexForElement(element);
        if (index !== -1) {
            this.records[index] = {...this.records[index], ...newRecord, element: element};
        } else {
            this.records.push({...newRecord, element: element});
        }
    }

    cleanupRecords() {
        this.records = this.records.filter(record => !record.element || document.contains(record.element));
    }

    getRecordsWithoutElements() {
        return this.records.map(({element, ...rest}) => rest);
    }

    isRecordRequired(record) {
        return FieldValidator.isElementRequired(record.element);
    }

    computeAllRequiredFieldsFilled() {
        const requiredRecords = this.records.filter(record => this.isRecordRequired(record));
        if (requiredRecords.length === 0) return true;
        
        for (const record of requiredRecords) {
            if (!FieldValidator.recordHasValue(record)) return false;
        }
        return true;
    }

    scheduleRequiredCheck() {
        if (this.collecting) return;
        if (this.initTimer) clearTimeout(this.initTimer);
        
        this.initTimer = setTimeout(() => {
            const newState = this.computeAllRequiredFieldsFilled();
            
            if (this.allRequiredFieldsFilled === newState) return;
            
            this.emitRequiredEvents(newState);
        }, this.initDebounceTimeout);
    }

    attachRequiredListener(element) {
        if (!FieldValidator.isElementRequired(element)) return;
        
        const events = FieldValidator.getElementEvents(element);
        const handler = () => {
            this.upsertElementRecord(element);
            
            if (FieldValidator.needsDebounce(element)) {
                this.debouncer.debounce(element, () => {
                    this.scheduleRequiredCheck();
                }, this.debounceTimeout);
            } else {
                this.scheduleRequiredCheck();
            }
        };
        
        if (this.requiredListenerManager.add(element, events, handler)) {
            this.upsertElementRecord(element);
        }
    }

    attachListener(element) {
        const events = FieldValidator.getElementEvents(element);
        const handler = () => this.upsertElementRecord(element);
        
        if (this.listenerManager.add(element, events, handler)) {
            this.upsertElementRecord(element);
        }
    }

    detachListener(element) {
        this.listenerManager.remove(element);
        this.requiredListenerManager.remove(element);
        this.debouncer.cancel(element);
    }

    collectFromComponentTree(component) {
        this.processFormElements(component);
        component.children.forEach(child => this.collectFromComponentTree(child));
    }

    attachToChildRecursively(component) {
        this.processFormElements(component);
        this.processChildrenRecursively(component, this.attachToChildRecursively);
    }

    detachFromChildRecursively(component) {
        this.getFormElements(component).forEach(element => {
            this.detachListener(element);
            const index = this.records.findIndex(record => record.element === element);
            if (index !== -1) this.records.splice(index, 1);
        });
        
        this.processChildrenRecursively(component, this.detachFromChildRecursively);
    }

    addChild(child) {
        const result = super.addChild(child);
        this.attachToChildRecursively(child);
        return result;
    }

    removeChild(child) {
        const result = super.removeChild(child);
        this.detachFromChildRecursively(child);
        return result;
    }

    destroy() {
        if (this.initTimer) clearTimeout(this.initTimer);
        this.debouncer.clear();
        this.listenerManager.clear();
        this.requiredListenerManager.clear();
        this.records = [];
        super.destroy();
    }
}