export default (withCss) =>
{
    return {
        error: withCss('make-color-error'),
        red: withCss('make-color-red'),
        dred: withCss('make-color-d-red'),
        blue: withCss('make-color-blue'),
        lblue: withCss('make-color-l-blue'),
        yellow: withCss('make-color-yellow'),
        green: withCss('make-color-green'),
    }
}