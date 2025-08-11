export default (Decorator) =>
    
function (fn, needReApply = false) {
    return (
        (...args) =>
        new Decorator(
            element => fn(element, ...args),
            needReApply
        )
    );
} 
