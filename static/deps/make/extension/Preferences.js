export default class Preferences {
    constructor(...options) {
        this.options = {};
        this.listToParse = [];

        options.forEach(opt => {
            if (Array.isArray(opt)) {
                this.listToParse = this.listToParse.concat(opt);
            } else if (opt && typeof opt === 'object') {
                Object.assign(this.options, opt);
            } else {
                this.listToParse.push(opt);
            }
        });
    }

    get(name, defaultValue = null) {
        return this.options[name] ? this.options[name] : defaultValue;
    }

    set(name, value, force = false) {
        if (force || !this.options[name]) {
            this.options[name] = value;
        }
        return this;
    }

    parse(...names) {
        if (names.length === 1) {
            if (typeof names[0] === 'string') {
                names = names[0].split(' ').filter(Boolean);
            }
            if (Array.isArray(names[0])) {
                names = names[0]
            }
        }

        const result = {};
        for (let i = 0; i < names.length; i++) {
            result[names[i]] = i < this.listToParse.length ? this.listToParse[i] : null;
        }

        this.options = Object.assign(this.options, result);
        return this;
    }
}
