export default (withCss) =>
{
    return {
        goose: withCss('make-goose'),
        noticeBody: withCss('make-notice-body'),
        textItalic: withCss('make-text-italic'),
        textBold: withCss('make-text-bold'),
        leftAlign: withCss('make-text-align-left'),
        simpleLink: withCss('make-simple-link'),

        flex: withCss('make-flex'),
        flexRow: withCss('make-flex-row'),
        flexColumn: withCss('make-flex-column'),
        gapped: withCss('gap-6px'),
        gap6px: withCss('make-gap-6px'),
        gap10px: withCss('make-gap-10px'),

        formGroup: withCss('make-form-group'),
        delayedMarginOnHover: withCss('make-delayed-margin-on-hover'),
        marginOnHover: withCss('make-margin-on-hover'),

        card: withCss('card'),
        body: withCss('card-body'),

        warning: withCss('btn', 'btn-warning', 'btn-sm'),
        danger: withCss('btn', 'btn-danger', 'btn-sm'),
        link: withCss('btn', 'btn-link'),
        primary: withCss('btn', 'btn-primary'),
        redir: withCss('make-btn-redir'),
        onConfirmationMargin: withCss('make-confirmation-margin'),
        
        shadeAtBorder: withCss('make-shade-at-border'),
        
        accordion: withCss('make-accordion'),
        accordionHeader: withCss('make-accordion-header'),
        accordionToggle: withCss('make-accordion-toggle'),
        accordionCollapse: withCss('make-accordion-collapse'),
        accordionContent: withCss('make-accordion-content'),
        accordionShow: withCss('make-accordion-show'),
        accordionCollapsed: withCss('make-accordion-collapsed'),
    }
}