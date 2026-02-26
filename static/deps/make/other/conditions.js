export default {
  'if': (condition, ...components) => condition ? components : [],
  callif: (condition, fn) => {
    const res = condition ? fn() : [];
    return Array.isArray(res) ? res : [res];
  },
  call: (fn) => {
    const res = fn();
    return Array.isArray(res) ? res : [res];
  },
  case: (condition, ...components) => ({ condition, components, endcase: false }),
  endcase: (...components) => ({ condition: undefined, components, endcase: true}),
  switch: (condition, ...cases) => {
    for (const c of cases) {
      if (c && condition === c.condition || c.endcase) {
        return c.components;
      }
    }
    return [];
  },
  callSwitch: (condition, ...cases) => {
    for (const c of cases) {
      if (c && condition === c.condition || c.endcase) {
        const res = c.components()
        return Array.isArray(res) ? res: [res]
      }
    }
    return [];
  },
}
