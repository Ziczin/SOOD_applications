export default (withStyle) => {
  const format = (v) => (typeof v === "number" ? `${v}px` : v);
  return {
    padding: (pad) => withStyle({ padding: format(pad) }),
    margin: (marg) => withStyle({ margin: format(marg) }),
    rounded: (rad) => withStyle({ borderRadius: format(rad) }),
    width: (w) => withStyle({ width: format(w) }),
    height: (h) => withStyle({ height: format(h) }),
    maxWidth: (w) => withStyle({ maxWidth: format(w) }),
    maxHeight: (h) => withStyle({ maxHeight: format(h) }),
    minWidth: (w) => withStyle({ minWidth: format(w) }),
    minHeight: (h) => withStyle({ minHeight: format(h) }),
    gap: (h) => withStyle({ gap: format(h) }),
  };
};
