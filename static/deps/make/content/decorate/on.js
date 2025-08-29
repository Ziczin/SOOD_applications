export default (Event) => 
{
    return {
        hover: Event('mouseenter', { passive: true }),
        dehover: Event('mouseleave', { passive: true }),
        click: Event('click', { passive: true }),
        focus: Event('focus', { passive: true }),
        defocus: Event('blur', { passive: true }),
        change: Event('change', { passive: true }),
    }
}