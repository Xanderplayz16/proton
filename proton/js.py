runpython = """

const scripts = document.querySelectorAll('script[type="text/python"]')
console.log("Python running...")
scripts.forEach(function(obj) {
    if (obj.hasAttribute('src')) {
        pywebview.api.evalpy_url(obj.getAttribute('src'))
    } else {
        pywebview.api.evalpy(obj.textContent)
    }
    
})

null"""