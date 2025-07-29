// Element.js
export class ElementBuilder {
  constructor(attrs = {}, content = '') {
    this.attrs = attrs
    this.content = content
    this.children = []
  }

  // Переопределяется в наследниках
  get tagName() {
    throw new Error('Override tagName in subclass')
  }

  // Добавить наследника
  addChild(childBuilder) {
    this.children.push(childBuilder)
    return this
  }

  // Построить элемент и рекурсивно его дочерние
  build() {
    const el = document.createElement(this.tagName)
    Object.entries(this.attrs).forEach(([k, v]) => el.setAttribute(k, v))
    if (this.content) el.textContent = this.content

    this.children.forEach(child => {
      el.append(child.build())
    })

    return el
  }
}

export class DivBuilder extends ElementBuilder {
  get tagName() { return 'div' }
}

export class PBuilder extends ElementBuilder {
  get tagName() { return 'p' }
}
