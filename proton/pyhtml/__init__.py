from ..core.utils import remove_indentation, is_url, get_hash
import requests
import threading
from typing import Any
class PyHTMLContext:
    def __init__(self, window, globals: dict[str, Any]) -> None:
        self._globals = globals
        self.window = window
        self.threads: list[threading.Thread] = []
        self.evalpy.__func__.__name__ = "evalpy"
        self.evalpy_url.__func__.__name__ = "evalpy_url"
        
    def evalpy(self, script: str) -> None:
        self._run(script)
    def evalpy_url(self, url: str) -> None:
        if is_url(url):
            r = requests.get(url)
            if r.status_code == 200:
                script: str = r.content.decode()
                self._run(script)
        else:
            if url.startswith('/'):
                # Absolute path
                host: str = self.window.webview.evaluate_js('location.host')
                protocol: str = self.window.webview.evaluate_js('location.protocol')
                r = requests.get(f"{protocol}//{host}{url}")
                if r.status_code == 200:
                    script = r.content.decode()
                    
                    self._run(script)
            else:
                # Relative path
                pass
    def _run(self, script: str):
        print(f"Running script {get_hash(script)}")
        self.threads.append(threading.Thread(target=exec,args=(remove_indentation(script), self._globals)))
        self.threads[-1].start()
    def expose(self):
        self.window.webview.expose(self.evalpy)
        self.window.webview.expose(self.evalpy_url)
            