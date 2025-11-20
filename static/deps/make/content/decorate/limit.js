export default (createDecorator) => {
	return {
		charactersWhiteList: createDecorator((component, allowedChars) => {
			const allowedMap = Object.create(null)
			for (let i = 0; i < allowedChars.length; i++) allowedMap[allowedChars[i]] = true

			const el = component.element
			el.addEventListener('keydown', function (event) {
				const key = event.key
				if (key.length === 1 && !allowedMap[key]) event.preventDefault()
			})

			el.addEventListener('paste', function (event) {
				const pasteText = (event.clipboardData || window.clipboardData).getData('text') || ''
				for (let i = 0; i < pasteText.length; i++) {
					if (!allowedMap[pasteText[i]]) { event.preventDefault(); return }
				}
			})

			el.addEventListener('input', function () {
				const currentValue = el.value
				if (!currentValue) return
				let filtered = ''
				for (let i = 0; i < currentValue.length; i++) {
					const ch = currentValue[i]
					if (allowedMap[ch]) filtered += ch
				}
				if (currentValue !== filtered) el.value = filtered
			})
		}, true),

		decimalPrecision: createDecorator((component, maxDecimals) => {
			const el = component.element
			if (!el || el.tagName !== 'INPUT' || el.type !== 'number') return

			const seps = ['.', ',']

			function findSepIndexAndChar(value) {
				for (let i = 0; i < seps.length; i++) {
					const idx = value.indexOf(seps[i])
					if (idx >= 0) return { idx, ch: seps[i] }
				}
				return { idx: -1, ch: '' }
			}

			el.addEventListener('input', function () {
				const currentValue = this.value
				if (!currentValue) return
				const { idx: sepIndex, ch: sepChar } = findSepIndexAndChar(currentValue)
				if (sepIndex === -1) return
				const integer = currentValue.slice(0, sepIndex)
				let frac = currentValue.slice(sepIndex + 1).replace(/[^0-9]/g, '')
				if (maxDecimals >= 0 && frac.length > maxDecimals) frac = frac.slice(0, maxDecimals)
				this.value = integer + sepChar + frac
			})

			el.addEventListener('blur', function () {
				const currentValue = this.value
				if (!currentValue) return
				const { idx: sepIndex, ch: sepChar } = findSepIndexAndChar(currentValue)
				if (sepIndex === -1) {
					if (maxDecimals === 0) return
					if (maxDecimals > 0) this.value = currentValue + sepChar + ''.padEnd(maxDecimals, '0')
					return
				}
				if (maxDecimals === 0) {
					this.value = currentValue.slice(0, sepIndex)
					return
				}
				const integer = currentValue.slice(0, sepIndex)
				let frac = currentValue.slice(sepIndex + 1).replace(/[^0-9]/g, '').slice(0, maxDecimals)
				if (frac.length < maxDecimals) frac = frac.padEnd(maxDecimals, '0')
				this.value = integer + sepChar + frac
			})
		}, true),
	}
}
