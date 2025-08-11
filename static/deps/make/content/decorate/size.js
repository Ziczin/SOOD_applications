
export default (withCss) =>
{
    return {
        small: withCss('make-size-small'),
        medium: withCss('make-size-medium'),
        large: withCss('make-size-large'),
    }
}