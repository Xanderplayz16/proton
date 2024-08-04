import webview as wv
import threading as th
import requests, os, random, hashlib, time, signal
from typing import Callable, Any
from .pyhtml.generate_globals import generateGlobals
from .utils import remove_indentation, is_url, null_lambda
from .pyhtml.document import Document
from .js import runpython


class Window:
    document: Document
    def __init__(self, name, path, frameless:bool=False, easy_drag:bool=False):
        #wv.DRAG_REGION_SELECTOR = "drag-region"
        self.webview = wv.create_window(name, os.path.join(path, 'index.html'), frameless=frameless, easy_drag=easy_drag)
        self._globals = generateGlobals(self) 
        self.document = self._globals["document"]
        def _evalpy(script):
            print(f"Running script {hashlib.sha1(script.encode()).hexdigest()[:7]}")
            #print(remove_indentation(script))
            exec(remove_indentation(script), self._globals)
        def _evalpy_url(url):
            if is_url(url):
                r = requests.get(url)
                if r.status_code == 200:
                    script = r.content.decode()
                    print(f"Running script {hashlib.sha1(script.encode()).hexdigest()[:7]}")
                    exec(remove_indentation(script), self._globals)
            else:
                pass
        _evalpy.__name__ = "evalpy"
        _evalpy_url.__name__ = "evalpy_url"
        self.webview.expose(_evalpy)
        self.webview.expose(_evalpy_url)
    
    def start(self, debug:bool = False, gui:str = "edgechromium"):
        """
        Starts the window.
        NOTE: THIS WILL DISABLE SIGNALS FOR ~20 MILLISECONDS AFTER THIS IF USING GTK!
        """
        self.port = random.randint(55556, 59999)
        self.wviewprocess = th.Thread(target=(lambda: wv.start(private_mode=True, debug=debug, http_port=self.port, gui=gui)), name="MainThread")
        if gui == "gtk":
            signal.signal = null_lambda
            signal_func = signal.signal
            def _reenable_signals():
                time.sleep(0.020)
                signal.signal = signal_func
            th.Thread(target=_reenable_signals).start()
        self.wviewprocess.start()
        self.webview.evaluate_js(runpython)
        
    def expose(self, func):
        """
        Exposes a Python function to Javascript.
        """
        self.webview.expose(func)
    def __del__(self):
        self.webview.destroy()
    def minimize(self):
        """
        Minimize the webview window.
        """
        self.webview.minimize()
    def maximize(self):
        """
        Maximize the webview window.
        """
        self.webview.maximize()
    @property
    def draggable(self) -> bool:
        """
        Returns true if the webview window is draggable, else return false.
        """
        return self.webview.draggable
    @property
    def html(self) -> str:
        """
        Returns the HTML of the current page.
        """
        return self.webview.html
    @property
    def on_top(self) -> bool:
        """
        Returns true if the webview window is on top, else return false.
        """
        return self.webview.on_top
    def hide(self) -> None:
        """
        Hides the window.
        """
        self.webview.hide()
    def show(self) -> None:
        """
        Shows the window.
        """
        self.webview.show()
    @property
    def hidden(self) -> bool:
        """
        Returns true if the window is hidden, else return false.
        """
        return self.webview.hidden
    def setsize(self, width: int, height: int) -> None:
        self.webview.set_window_size(width, height)
    @property
    def height(self) -> int:
        """
        Returns the height of the window.
        """
        return self.webview.height
    @property
    def width(self) -> int:
        """
        Returns the width of the webview window.
        """
        return self.webview.width
    def evaluate_js(self, script: str, callback: Callable | None = None) -> Any:
        """
        Evaluates the given javascript, and calls callback when any promises were completed.
        """
        return self.webview.evaluate_js(script=script, callback=callback)
        

    