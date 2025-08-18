export default (withStyle) =>
{
    return {
        padding: (pad) => withStyle({
            padding: `${pad}px`,
        }),
        margin: (marg) => withStyle({
            margin: `${marg}px`,
        }),
    }
}