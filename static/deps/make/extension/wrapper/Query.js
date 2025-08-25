export default class Query {
    constructor(...args) {
        let route, method, baseHeaders, baseBody, redirect_request_key;
        
        if (args.length === 1 && typeof args[0] === 'object' && 'route' in args[0]) {
            const options = args[0];
            route = options.route;
            method = options.method ?? null;
            baseHeaders = options.baseHeaders || {};
            baseBody = options.baseBody || {};
            redirect_request_key = options.redirect_request_key ?? null;
        } else {
            [route, method = null, baseHeaders = {}, baseBody = {}, redirect_request_key = null] = args;
        }
        
        this._baseRoute = route;
        this._method = method;
        this._baseHeaders = baseHeaders;
        this._baseBody = baseBody;
        this._redirect_request_key = redirect_request_key;

        this._route = [];
        this._headers = {};
        this._body = {};
        this._mergedBody = null;
        this._queryParams = null;
        this._queryString = '';
    }

    at(param) {
        this._route.push(param);
        return this;
    }

    as(method) {
        this._method = method;
        return this;
    }

    via(header) {
        this._headers = { ...this._headers, ...header };
        return this;
    }

    with(body) {
        this._body = { ...this._body, ...body };
        this._queryString = '';

        if (this._method && String(this._method).toUpperCase() === 'GET') {
            const source = { ...this._baseBody, ...this._body };
            const pairs = [];

            const encode = (k, v) => encodeURIComponent(k) + '=' + encodeURIComponent(String(v));

            const processValue = (key, val) => {
                if (val === undefined || val === null) return;
                if (Array.isArray(val)) {
                    for (let i = 0; i < val.length; i++) {
                        const item = val[i];
                        if (item === undefined || item === null) continue;
                        if (typeof item === 'object' && !Array.isArray(item)) {
                            for (const subKey of Object.keys(item)) {
                                const subVal = item[subKey];
                                if (subVal === undefined || subVal === null) continue;
                                pairs.push(encode(`${key}[${i}].${subKey}`, subVal));
                            }
                        } else {
                            pairs.push(encode(`${key}[${i}]`, item));
                        }
                    }
                } else if (typeof val === 'object') {
                    for (const subKey of Object.keys(val)) {
                        const subVal = val[subKey];
                        if (subVal === undefined || subVal === null) continue;
                        pairs.push(encode(`${key}.${subKey}`, subVal));
                    }
                } else {
                    pairs.push(encode(key, val));
                }
            };

            for (const key of Object.keys(source)) {
                processValue(key, source[key]);
            }

            this._queryString = pairs.join('&');
        }

        return this;
    }

    mergeBodies() {
        this._mergedBody = { ...this._baseBody, ...this._body };
        return this;
    }

    clearBody() {
        this._body = {};
        return this;
    }

    clearHeaders() {
        this._headers = {};
        return this;
    }

    clearRoute() {
        this._route = [];
        return this;
    }

    clearMergedBody() {
        this._mergedBody = null;
        return this;
    }

    clear() {
        this._route = [];
        this._headers = {};
        this._body = {};
        this._mergedBody = null;
        this._queryString = '';
        return this;
    }

    copy(deep = false) {
        const currentHeaders = { ...this._baseHeaders, ...this._headers };
        const currentBody = { ...this._baseBody, ...this._body };

        let newBaseHeaders = currentHeaders;
        let newBaseBody = currentBody;

        if (deep) {
            newBaseHeaders = { ...currentHeaders };
            newBaseBody = { ...currentBody };
        }

        return new Query(
            this._buildRoute(),
            this._method,
            newBaseHeaders,
            newBaseBody,
            this._redirect_request_key
        );
    }

    async fetch() {
        const url = this._buildRoute() + '/';
        const headers = this._buildHeaders();
        const body = this._mergedBody !== null 
            ? this._mergedBody 
            : this._buildBody();
        
        const options = {
            method: this._method,
            headers: {
                'Content-Type': 'application/json',
                ...headers,
            }
        };

        if (Object.keys(body).length > 0) {
            options.body = JSON.stringify(body);
        }

        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();

        if (this._redirect_request_key && this._redirect_request_key in data) {
            window.location.href = data[this._redirect_request_key];
        }
        
        return data;
    }

    _buildRoute() {
        let result = this._baseRoute;
        for (const param of this._route) {
            result += '/' + encodeURIComponent(param);
        }
        if (this._queryString && this._queryString.length > 0) {
            result += (result.includes('?') ? '&' : '?') + this._queryString;
        }
        return result;
    }

    _buildBody() {
        return { ...this._baseBody, ...this._body };
    }

    _buildHeaders() {
        return { ...this._baseHeaders, ...this._headers };
    }

    getState() {
        return {
            route: this._buildRoute(),
            headers: this._buildHeaders(),
            body: this._buildBody(),
            method: this._method,
            mergedBody: this._mergedBody
        };
    }
}
