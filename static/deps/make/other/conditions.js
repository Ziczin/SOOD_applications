export default {
  'if': (condition, ...components) => condition ? components : [],
  callif: (condition, fn) => {
    const res = condition ? fn() : [];
    return Array.isArray(res) ? res : [res];
  },
  case: (condition, ...components) => ({ condition, components }),
  switch: (...cases) => {
    for (const c of cases) {
      if (c && c.condition) {
        return c.components;
      }
    }
    return [];
  },
  callSwitch: (...cases) => {
    for (const c of cases) {
      if (c && c.condition) {
        const res = c.components()
        return Array.isArray(res) ? res: [res]
      }
    }
    return [];
  },
}
