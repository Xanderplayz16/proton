import webview as wv
import threading as th
from .pyhtml.generate_globals import generateGlobals
import hashlib
import random
import requests
import typing
from .utils import remove_indentation, is_url
from .pyhtml.document import Document
from .js import runpython

class Window:
    document: Document
    def __init__(self, name, path, frameless:bool=False, easy_drag:bool=False):
        #wv.DRAG_REGION_SELECTOR = "drag-region"
        self.webview = wv.create_window(name, f"{path}/index.html", frameless=frameless, easy_drag=easy_drag)
        self._globals = generateGlobals(self) 
        self.document = self._globals["document"]
        def evalpy(script):
            print(f"Running script {hashlib.sha1(script.encode()).hexdigest()[:7]}")
            #print(remove_indentation(script))
            exec(remove_indentation(script), self._globals)
        def evalpy_url(url):
            if is_url(url):
                r = requests.get(url)
                if r.status_code == 200:
                    script = r.content.decode()
                    print(f"Running script {hashlib.sha1(script.encode()).hexdigest()[:7]}")
                    exec(remove_indentation(script), self._globals)
            else:
                pass
        self.webview.expose(evalpy)
        self.webview.expose(evalpy_url)
    
    def start(self, debug:bool = False, gui:str = "edgechromium"):
        """Starts the window."""
        self.port = random.randint(55556, 59999)
        self.wviewprocess = th.Thread(target=wv.start, kwargs = {"private_mode": True, "debug": debug, "http_port": self.port, "gui": gui}, name="MainThread")
        self.wviewprocess.start()
        self.webview.evaluate_js(runpython)
    def expose(self, func):
        self.webview.expose(func)
    def __del__(self):
        self.webview.destroy()
    def minimize(self):
        self.webview.minimize()
    def maximize(self):
        self.webview.maximize()
    @property
    def draggable(self):
        return self.webview.draggable
    @property
    def html(self):
        return self.webview.html
    @property
    def on_top(self):
        return self.webview.on_top
    def hide(self):
        self.webview.hide()
    def show(self):
        self.webview.show()
    @property
    def hidden(self):
        return self.webview.hidden
    def setsize(self, width: int, height: int):
        self.webview.set_window_size(width, height)
    @property
    def height(self):
        return self.webview.height
    @property
    def width(self):
        return self.webview.width
    def destroy(self):
        self.webview.destroy()
    def evaluate_js(self, script: str, callback: typing.Callable | None = None):
        return self.webview.evaluate_js(script=script, callback=callback)

    