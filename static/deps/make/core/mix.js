export default function mix(Base, ...mixins) {
    class Mixed extends Base {}

    for (const mixin of mixins) {
        Object.getOwnPropertyNames(mixin.prototype).forEach((name) => {
            if (name === "constructor") return;

            if (!Mixed.prototype.hasOwnProperty(name)) {
                Object.defineProperty(
                    Mixed.prototype,
                    name,
                    Object.getOwnPropertyDescriptor(mixin.prototype, name)
                );
            }
        });

        Object.getOwnPropertyNames(mixin).forEach((name) => {
            if (["prototype", "name", "length"].includes(name)) return;

            if (!Mixed.hasOwnProperty(name)) {
                Object.defineProperty(
                    Mixed,
                    name,
                    Object.getOwnPropertyDescriptor(mixin, name)
                );
            }
        });
    }

    return Mixed;
}