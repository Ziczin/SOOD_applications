import makeWith from "./with.js";

export default (withCss) =>
{
    return {
        separator: withCss('make-block-separator'),
        scrollbox: withCss('make-scrollbox')
    }
}