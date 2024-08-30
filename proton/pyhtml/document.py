import webview as wv
from ..core.utils import toObject
class Document: # TODO: Implement the -Nss- -Ns's- NSs'?
    def __init__(self, window):
        self.webview: wv.Window = window.webview
    
    @property
    def body(self):
        """Returns the <body> object."""
        return self.querySelector("body")

    @property
    def head(self):
        """Returns the <head> object."""
        return self.querySelector("head")
    
    def querySelector(self, selector) -> list:
        """Returns the first object that matches the selector."""
        return self.webview.dom.get_elements(selector)[0]

    def querySelectorAll(self, selector) -> list:
        """Returns all of the objects that match the selector."""
        return self.webview.dom.get_elements(selector)
    
    @property
    def characterSet(self) -> str:
        """Returns the character set."""
        return self.webview.evaluate_js("document.characterSet")
    
    @property
    def childElementCount(self) -> int:
        """Returns the number of children that the Document has. Usually 1."""
        return self.webview.evaluate_js("document.childElementCount")
    
    @property
    def children(self):
        """Returns the children that the Document has. Usually just 1."""
        return self.webview.evaluate_js("document.children")
    
    @property
    def compatMode(self) -> str:
        """Returns BackCompat if quirks mode is enabled, and CSS1Compat if quirks is disabled."""
        return self.webview.evaluate_js("document.compatMode")
    
    @property
    def contentType(self) -> str:
        """Returns the MIME type of the current page."""
        return self.webview.evaluate_js("document.contentType")
    
    # TODO: defaultView
    @property
    def designMode(self) -> str:
        return self.webview.evaluate_js('document.designMode')
    
    @designMode.setter
    def designModeSetter(self, val: str) -> None:
        self.webview.evaluate_js('document.designMode = ' + val)
    
    @property
    def cookie(self) -> str:
        return self.webview.evaluate_js("document.cookie")
    
    @property
    def currentScript(self) -> str:
        return "PythonScript"
    
    @cookie.setter
    def cookiesetter(self, val) -> None:
        self.webview.evaluate_js("document.cookie = " + val)
    
    @property
    def dir(self):
        return self.webview.evaluate_js("document.dir")
    
    @property
    def doctype(self):
        """Returns the Document Type Declaration (DTD) in a object."""
        return toObject(self.webview.evaluate_js("document.doctype"))
    
    @property
    def documentElement(self):
        """Returns the <html> object."""
        return self.querySelector("html")
    
    @property
    def documentURI(self) -> str:
        """Returns the current URI of the page."""
        return self.doctype.baseURI
    
    # TODO: Implement embeds
    @property
    def firstElementChild(self):
        """Returns the <html> object."""
        return self.querySelector("html")
    # TODO: Implement forms+
    
    @property
    def fonts(self):
        """Returns all of the fonts."""
        return toObject(self.webview.evaluate_js("document.fonts"))
    
    @property
    def forms(self):
        return self.querySelectorAll("forms")
    
    def append(self, element) -> None:
        """Appends an object to the document. Accepts any object with an __str__ function."""
        self.webview.dom.document.append(element)
    
    def createElement(self, html):
        """Creates an element."""
        return self.webview.dom.create_element(html)
    
    def getElementById(self, id) -> list:
        """Returns the elements with the specified name."""
        return self.querySelectorAll("#" + id)
    
    def getElementsByName(self, name) -> list:
        """Returns the elements with the specified name."""
        return self.querySelectorAll(f"[name={name}]")
    
    def getElementsByTagName(self, name) -> list:
        """Returns the elements with the specificed tag name."""
        return self.querySelectorAll(name)
