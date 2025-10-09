export default class Event {
  constructor({ret}={}) {
    this.subscribers = []
    this.ret = ret ? ret : this
  }

  emit(...args) {
    this.subscribers.map((s) => s(...args))
    return this.ret
  }

  sub(fn) {
    this.subscribers.push(fn)
    return this.ret
  }

  unsub(fn) {
    const i = this.subscribers.indexOf(fn)
    if (i !== -1) this.subscribers.splice(i, 1)
    return this.ret
  }
}
