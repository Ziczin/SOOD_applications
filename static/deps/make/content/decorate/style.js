export default (withStyle) =>
{
    return {
        padding: (pad) => withStyle({
            padding: `${pad}px`,
        }),
        margin: (marg) => withStyle({
            margin: `${marg}px`,
        }),
        rounded: (rad) => withStyle({
            borderRadius: `${rad}px`,
        }),
        width: (w) => withStyle({
            width: `${w}px`,
        }),
        height: (h) => withStyle({
            height: `${h}px`,
        }),
        maxWidth: (w) => withStyle({
            maxWidth: `${w}px`,
        }),
        maxHeight: (h) => withStyle({
            maxHeight: `${h}px`,
        }),
        gap: (h) => withStyle({
            gap: `${h}px`,
        }),
    }
}