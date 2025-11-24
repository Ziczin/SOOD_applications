export default class Event {
  constructor({ret}={}) {
    this.subscribers = []
    this.oneSubscribers = []
    this.ret = ret ? ret : this
  }

  emit(...args) {
    this.subscribers.map((s) => s(...args))
    this.oneSubscribers.map((s) => s(...args))
    this.oneSubscribers = []
    return this.ret
  }

  sub(fn) {
    this.subscribers.push(fn)
    return this.ret
  }

  once(fn) {
    this.oneSubscribers.push(fn)
    return this.ret
  }

  unsub(fn) {
    const i = this.subscribers.indexOf(fn)
    if (i !== -1) this.subscribers.splice(i, 1)
    const j = this.oneSubscribers.indexOf(fn)
    if (j !== -1) this.oneSubscribers.splice(j, 1)
    return this.ret
  }
}
