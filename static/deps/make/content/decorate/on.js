export default (event) => 
{
    const basic = event.basic
    const custom = event.custom
    return {
        hover: basic('mouseenter'),
        dehover: basic('mouseleave'),
        focus: basic('focus'),
        defocus: basic('blur'),
        click: basic('click'),
        change: basic('change'),
        input: basic('input'),
        keydown: basic('keydown'),
        paste: basic('paste'),
        submit: basic('submit'),
        inputTimeOut: custom(
        (time, foo) => {
            let timer = null;

            function clearTimer() {
                if (timer !== null) {
                    clearTimeout(timer);
                timer = null;
                }
            }

            function startOrRefresh(e) {
                clearTimer();
                timer = setTimeout(() => {
                    timer = null;
                    foo(e);
                }, time);
            }

            function onBlur(e) {
                if (timer !== null) {
                    clearTimer();
                    foo(e);
                }
            }

            return [{
                eventType: 'input',
                handler: startOrRefresh,
            }, {
                eventType: 'blur',
                handler: onBlur,
            }]
        })
    }
}