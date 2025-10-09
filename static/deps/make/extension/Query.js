class BaseObjManager {
    constructor(base = {}) {
        this.base = base
        this.container = {}
    }
    add(elem) {
        if (typeof elem === 'object') {
            this.container = Object.assign(this.container, elem)
        }
    }
    get() { return Object.assign(this.container, this.base) }
    view() { let res = new BaseObjManager(this.get()); this.flush(); return res }
    flush() { this.container = {}; return this}
    clear() { this.base = {}; return this }
}

class BaseArrManager {
    constructor(base = []) {
        this.base = base
        this.container = []
    }
    add(elem) {
        this.container = [...this.container, elem]
    }
    get() { return [...this.base, ...this.container] }
    view() { let res = new BaseArrManager(this.get()); this.flush(); return res }
    flush() { this.container = []; return this }
    clear() { this.base = []; return this }
}

class RouteManager extends BaseArrManager {
    build() { return this.get().join('/') + '/'; }
    view() { let res = new RouteManager(this.get()); this.flush(); return res }
}

class QueryManager extends BaseObjManager {
    view() { let res = new QueryManager(this.get()); this.flush(); return res }
    build() {
        const parts = [];
        const enc = encodeURIComponent;
        const src = this.get();

        Object.entries(src).forEach(([key, value]) => {
            let str = value
            if (!(typeof value === 'string')) {
                str = typeof value === 'object' ? JSON.stringify(value) : String(value);
            }
            parts.push(`${enc(key)}=${enc(str)}`);
        });
        return parts.length ? `?${parts.join('&')}` : '';
    }
}

export default class Query {
    constructor(route, query, header, body) {
        this.route = route;
        this.query = query;
        this.header = header;
        this.body = body;
    }
    
    static new(baseRoute=[], baseQuery={}, baseHeader={}, baseBody={}) {
        if (!Array.isArray(baseRoute)) {baseRoute = [baseRoute]}
        return new Query(
            new RouteManager(baseRoute),
            new QueryManager(baseQuery),
            new BaseObjManager(baseHeader),
            new BaseObjManager(baseBody),
        );
    }

    view() {
        return new Query(
            this.route.view(),
            this.query.view(),
            this.header.view(),
            this.body.view(),
        );
    }

    flush() {
        this.route.flush(),
        this.query.flush(),
        this.header.flush(),
        this.body.flush()
        return this
    }

    at(elem) { this.route.add(elem); return this; }
    via(elem) { this.header.add(elem); return this; }
    with(elem) { this.body.add(elem); return this; }
    where(elem) { this.query.add(elem); return this; }

    async get() { return await this.fetch('GET') }
    async post() { return await this.fetch('POST') }
    async patch() { return await this.fetch('PATCH') }
    async delete() { return await this.fetch('DELETE') }
    async put() { return await this.fetch('PUT') }

    async fetch(method=null) {
        const route = this.route.build();
        const query = this.query.build();
        const url = route + query;
        const headers = this.header.get();
        const body = this.body.get();
        
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                ...headers,
            }
        };

        if (method !== 'GET') {
            options.body = JSON.stringify(body);
        }

        const response = await fetch(url, options);
        this.flush()

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

        return data;
    }
}
