import webview as wv
import threading as th
import os, random, time, signal
from typing import Callable, Any
from ..pyhtml.generate_globals import generateGlobals
from ..pyhtml import PyHTMLContext
from .utils import null_lambda
from .js import runpython


class Window:
    def __init__(self, name, path, frameless: bool = False, easy_drag: bool = False) -> None:
        self.webview = wv.create_window(name, os.path.join(path, 'index.html'), frameless=frameless, easy_drag=easy_drag)
        self._globals = generateGlobals(self)
        self.document = self._globals["document"]
        self.pycontext = PyHTMLContext(self,self._globals)
        
        self.pycontext.expose()
    
    def start(self, debug: bool = False, gui: str = "edgechromium") -> None:
        """
        Starts the window.
        NOTE: THIS WILL DISABLE SIGNALS FOR ~200 MILLISECONDS AFTER THIS IF USING GTK!
        """
        self.port = random.randint(55556, 59999)
        self.wviewprocess = th.Thread(target=(lambda: wv.start(private_mode=True, debug=debug, http_port=self.port, gui=gui)), name="MainThread")
        if gui == "gtk":
            signal_func = signal.signal
            signal.signal = null_lambda
            
            def _reenable_signals():
                time.sleep(0.200)
                signal.signal = signal_func
            th.Thread(target=_reenable_signals).start()
        self.wviewprocess.start()
        self.webview.evaluate_js(runpython)
        
    def expose(self, func):
        """
        Exposes a Python function to Javascript.
        """
        self.webview.expose(func)
        return func
    def __del__(self):
        self.webview.destroy()
    def minimize(self) -> None:
        """
        Minimize the webview window.
        """
        self.webview.minimize()
    def maximize(self) -> None:
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
        Evaluates the given javascript, and calls callback when any promises were resolved.
        """
        return self.webview.evaluate_js(script=script, callback=callback)
        
    @property
    def events(self): 
        """
        Returns a container containing all of the DOM events.
        """
        return self.webview.events

    