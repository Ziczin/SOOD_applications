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


    get() { return this.fetch('GET') }
    post() { return this.fetch('POST') }
    patch() { return this.fetch('PATCH') }
    delete() { return this.fetch('DELETE') }
    put() { return this.fetch('PUT') }

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
        const text = await response.text();
        const parsed = (() => {
            try {
                return text ? JSON.parse(text) : {};
            } catch (err) {
                return null;
            }
        })();
        data = parsed === null ? text : parsed;

        return data;
    }

    repeat(delay, method, func) {
        let intervalId = null;

        const schedule = (d) => {
            if (intervalId !== null) clearInterval(intervalId);
            intervalId = setInterval(async () => {
                const res = await this.view().fetch(method);
                if (res.stop) {
                    clearInterval(intervalId);
                    intervalId = null;
                    return;
                }
                if (res.response) {
                    func(res.response);
                    return;
                }
                if (res.delay && typeof res.delay === 'number' && res.delay > 0) {
                    schedule(res.delay);
                }
            }, d);
        };

        schedule(delay);

        return () => {
            if (intervalId !== null) {
                clearInterval(intervalId);
                intervalId = null;
            }
        };
    }



}
