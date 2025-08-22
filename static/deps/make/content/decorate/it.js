export default (withCss) =>
{
    return {
        goose: withCss('make-goose'),
        content: withCss('make-content'),
        contented: withCss('make-contented'),
        noticeBody: withCss('make-notice-body'),
        textItalic: withCss('make-text-italic'),
        textBold: withCss('make-text-bold'),
        leftAlign: withCss('make-text-align-left'),
        simpleLink: withCss('make-simple-link'),
        cardHeader: withCss('make-card-header-additional'),
        cardContent: withCss('make-card-content-additional'),

        flex: withCss('make-flex'),
        flexRow: withCss('make-flex-row'),
        flexColumn: withCss('make-flex-column'),
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
    }
}