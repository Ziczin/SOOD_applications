export default (make) =>
async function imp(path, ...other) {
  const mod = await import(path);
  return mod.default(make, ...other);
}