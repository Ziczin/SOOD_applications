export default class Decorator {
    constructor(func, needReApply = true) {
        this.func = func;
        this.needReApply = needReApply;
        this.applied = false;
    }
    
    apply(component) {
        if (this.needReApply || !this.applied) {
            this.func(component);
            this.applied = true;
        }
    }
}