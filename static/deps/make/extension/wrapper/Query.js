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
            this._queryString = this._buildQueryStringFrom(source);
        }

        return this;
    }

    where(params) {
        this._queryParams = { ...this._queryParams, ...params };
        this._queryString = this._buildQueryStringFrom(this._queryParams || {});
        return this;
    }

    _buildQueryStringFrom(source = {}) {
        const pairs = [];
        const encode = (k, v) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`;

        const walk = (key, val) => {
            if (val === undefined || val === null) return;
            if (Array.isArray(val)) {
                val.forEach((item, i) => {
                    const newKey = `${key}[${i}]`;
                    if (typeof item === 'object' && item !== null) {
                        walk(newKey, item);
                    } else {
                        pairs.push(encode(newKey, item));
                    }
                });
            } else if (typeof val === 'object') {
                Object.keys(val).forEach(sub => {
                    walk(`${key}[${encodeURIComponent(sub)}]`, val[sub]);
                });
            } else {
                pairs.push(encode(key, val));
            }
        };

        Object.keys(source).forEach(k => walk(k, source[k]));
        return pairs.join('&');
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
        this._queryParams = null;
        this._queryString = '';
        return this;
    }

    view() {
        const currentHeaders = { ...this._baseHeaders, ...this._headers };
        const currentBody = { ...this._baseBody, ...this._body };

        const snapshot = new Query(
            this._buildRoute(),
            this._method,
            currentHeaders,
            currentBody,
            this._redirect_request_key
        );

        this.clear()
        return snapshot;
    }
    clear() {
        this._route = [],
        this._headers = {},
        this._body = {},
        this._mergedBody = null,
        this._queryParams = null,
        this._queryString = '';
    }


    copy() {
        const q = new Query(
            this._baseRoute,
            this._method,
            { ...this._baseHeaders },
            { ...this._baseBody },
            this._redirect_request_key
        );
        q._route = [...this._route];
        q._headers = { ...this._headers };
        q._body = { ...this._body };
        q._mergedBody = this._mergedBody === null ? null : { ...this._mergedBody };
        q._queryParams = this._queryParams === null ? null : { ...this._queryParams };
        q._queryString = this._queryString;
        return q;
    }

    async get() {
        return await this.fetch('GET')
    }
    async post() {
        return await this.fetch('POST')
    }
    async put() {
        return await this.fetch('PUT')
    }
    async delete() {
        return await this.fetch('DELETE')
    }
    async patch() {
        return await this.fetch('PATCH')
    }

    async fetch(method=null) {
        let url = this._buildRoute();
        if (!url.includes('?')) {
            url += '/'
        }
        const headers = this._buildHeaders();
        const body = this._mergedBody !== null 
            ? this._mergedBody 
            : this._buildBody();
        
        const options = {
            method: method ?? this._method,
            headers: {
                'Content-Type': 'application/json',
                ...headers,
            }
        };

        if (Object.keys(body).length > 0) {
            options.body = JSON.stringify(body);
        }

        this.clear()
        const response = await fetch(url, options);
        
        let data;
        try {
            const text = await response.text();
            try {
                data = text ? JSON.parse(text) : {};
            } catch (err) {
                data = text;
            }
        }
        catch (error) {
            console.error('Make-Query error:', error);
            data = null;
        }

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
            result += (result.includes('?') ? '&' : '/?') + this._queryString;
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
