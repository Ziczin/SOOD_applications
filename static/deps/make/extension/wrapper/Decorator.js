import Applicable from '../mixin/Applicable.js';

export default class Decorator extends Applicable {
    constructor(func, needReApply = true) {
        super(); // Важно оставить super()
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