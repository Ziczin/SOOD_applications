export default function(createComponent, makeInner) {
    return {
        Separator: (...d) => createComponent('div', makeInner.separator, ...d),
        Scrollbox: (...d) => createComponent('div', makeInner.scrollbox, ...d),
    }
}
   
        
        
