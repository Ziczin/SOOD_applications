export default (event, delay) => 
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
        inputTimeOut: custom(
        (time, foo) => {
            let timer = null;

            function clearTimer() {
                if (timer !== null) {
                    clearTimeout(timer);
                timer = null;
                }
            }

            function startOrRefresh() {
                clearTimer();
                timer = setTimeout(() => {
                    timer = null;
                    foo();
                }, time);
            }

            function onBlur() {
                if (timer !== null) {
                    clearTimer();
                    foo();
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