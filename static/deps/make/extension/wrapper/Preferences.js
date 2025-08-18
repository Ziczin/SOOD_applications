export default class Preferences {
    constructor(options = {}) {
        this.options = { ...options };
    }

    get(name, defaultValue = null) {
        return this.options.hasOwnProperty(name) ? this.options[name] : defaultValue;
    }

    set(name, value, force = false) {
        if (!this.options.hasOwnProperty(name) || force) {
            this.options[name] = value;
        }
        return this; // Для цепочки вызовов
    }
}