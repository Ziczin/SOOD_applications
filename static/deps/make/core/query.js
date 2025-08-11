export default async function query(route, method, data = null) {
    method = method.toUpperCase();
    const options = { method };
    
    if (method === 'GET' && data) {
        const params = new URLSearchParams(data).toString();
        route = `${route}?${params}`;
    } else if (data) {
        options.headers = { 'Content-Type': 'application/json' };
        options.body = JSON.stringify(data);
    }
    
    const response = await fetch(route, options);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
}