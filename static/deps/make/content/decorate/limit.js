export default (createDecorator) =>
{
    return {
        charactersWhiteList: createDecorator(
            (component, allowedChars) => {
                const allowedMap = {};
                for (let idx = 0; idx < allowedChars.length; idx++) allowedMap[allowedChars[idx]] = true;
                component.element.addEventListener('keydown', function(event) {
                    const key = event.key;
                    if (key.length > 1) return;
                    if (!allowedMap[key]) event.preventDefault();
                });

                component.element.addEventListener('paste', function(event) {
                    const pasteText = (event.clipboardData || window.clipboardData).getData('text');
                    for (let idx = 0; idx < pasteText.length; idx++) {
                    if (!allowedMap[pasteText[idx]]) { event.preventDefault(); return; }
                    }
                });

                component.element.addEventListener('input', function() {
                    const currentValue = component.element.value;
                    let filtered = '';
                    for (let idx = 0; idx < currentValue.length; idx++) {
                    const ch = currentValue[idx];
                    if (allowedMap[ch]) filtered += ch;
                    }
                    if (component.element.value !== filtered) component.element.value = filtered;
                });
            }, true
        ),
    }
}