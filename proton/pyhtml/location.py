import webview as wv
class Location:
    def __init__(self, webview: wv.Window) -> None:
        self.webview = webview
    @property
    def href(self):
        return self.webview.evaluate_js('location.href')
    @property
    def host(self):
        return self.webview.evaluate_js('location.host')
    @property
    def hostname(self):
        return self.webview.evaluate_js('location.hostname')
    @property
    def port(self):
        return self.webview.evaluate_js('location.port')
    @property
    def pathname(self):
        return self.webview.evaluate_js('location.pathname')
    @property
    def search(self):
        return self.webview.evaluate_js('location.search')
    @property
    def hash(self):
        return self.webview.evaluate_js('location.hash')
    @property
    def origin(self):
        return self.webview.evaluate_js('location.origin')
    def assign(self, url: str):
        self.webview.evaluate_js(f'location.assign("{url}")')
    def reload(self):
        self.webview.evaluate_js(f'location.reload()')