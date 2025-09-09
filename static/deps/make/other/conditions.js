export default {
    'if': (condition, ...components) => condition ? components : [],
    case: (condition, ...components) => ({ condition, components }),
    switch: (...cases) => {
        for (const c of cases) {
            if (c.condition) {
                return c.components;
            }
        }
        return [];
    },
}