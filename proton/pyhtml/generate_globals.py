from .document import Document

def generateGlobals(self):
    alert = lambda message: self.webview.evaluate_js(f"alert({'"'}{message}{'"'})")
    document = Document(self)
    return {"alert": alert, "document": document, "window": self}

