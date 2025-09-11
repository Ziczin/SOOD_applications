export default (withCss) =>
{
    return {
        error: withCss('make-color-error'),
        red: withCss('make-color-red'),
        dred: withCss('make-color-d-red'),
        blue: withCss('make-color-blue'),
        lblue: withCss('make-color-l-blue'),
        yellow: withCss('make-color-yellow'),
        lyellow: withCss('make-color-l-yellow'),
        green: withCss('make-color-green'),
        lgreen: withCss('make-color-l-green'),
        lgray: withCss('make-color-l-gray'),
        mgray: withCss('make-color-m-gray'),
        dgray: withCss('make-color-d-gray'),
        vgray: withCss('make-color-v-gray'),
        white: withCss('make-color-white'),
    }
}