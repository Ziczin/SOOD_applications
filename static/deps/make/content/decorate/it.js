export default (withCss) =>
{
    return {
        goose: withCss('make-goose'),
        textItalic: withCss('make-text-italic'),
        leftAlign: withCss('make-text-align-left'),
        simpleLink: withCss('make-simple-link'),

        flex: withCss('make-flex'),
        flexRow: withCss('make-flex-row'),
        flexColumn: withCss('make-flex-column'),
        gapped: withCss('gap-6px'),
        gap6px: withCss('make-gap-6px'),
        gap10px: withCss('make-gap-10px'),

        formGroup: withCss('make-form-group'),
        beautySelect: withCss('make-beauty-select'),

        card: withCss('card'),
        body: withCss('card-body'),

        warning: withCss('btn', 'btn-warning', 'btn-sm'),
        danger: withCss('btn', 'btn-danger', 'btn-sm'),
        link: withCss('btn', 'btn-link'),
        primary: withCss('btn', 'btn-primary'),
        onConfirmationMargin: withCss('make-confirmation-margin'),
        
        shadeAtBorder: withCss('make-shade-at-border'),
    }
}