## LANG - RU

Make.js – библиотека-обёртка для работы с DOM в декларативном стиле, которая позволяет быстро выстраивать структуру страницы из JS на основе готовых шаблонов.

Как использовать:
1. Скачайте или склонируйте репозиторий в каталог со статическими файлами проекта.
2. Настройте сервер или фреймворк на раздачу статических файлов.
3. Подключите CSS:  
```html
<link rel="stylesheet" href="ПУТЬ_К_CSS">
```  
Например, в Django:  
```html
<link rel="stylesheet" href="{% static 'make/make.css' %}">
```
4. Вставьте на страницу тег для модульных скриптов:  
```html
<script type="module"> … </script>
```
5. Внутри этого тега импортируйте Make.js:  
```javascript
await import("ПУТЬ_К_JS");
```  
Например, в Django:  
```javascript
await import("{% static 'make/make.js' %}");
```
6. После импорта все функции и объекты библиотеки будут доступны через глобальный объект `make`.

---

## LANG - EN

Make.js – a wrapper library for declarative DOM manipulation that lets you quickly build page structures in JS using predefined templates.

How to use:
1. Download or clone the repository into your project's static files directory.
2. Configure your server or framework to serve static files.
3. Include the CSS:  
```html
<link rel="stylesheet" href="PATH_TO_CSS">
```  
For example, in Django:  
```html
<link rel="stylesheet" href="{{% static 'make/make.css' %}}">
```
4. Add a module script tag to your HTML page:  
```html
<script type="module"> … </script>
```
5. Inside that tag, import Make.js:  
```javascript
await import("PATH_TO_JS");
```  
For example, in Django:  
```javascript
await import("{{% static 'make/make.js' %}}");
```
6. After import, all library functions and objects are available via the global `make` object.
