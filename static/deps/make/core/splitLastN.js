export default (arr = [], n = 1) => {
  if (n <= 0) return [arr.slice(), []];
  const k = Math.min(n, arr.length);
  const idx = arr.length - k;
  return [arr.slice(0, idx), arr.slice(idx)];
};
