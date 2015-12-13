from .view import View
from PyQt4 import QtWebKit


class AbstractHtmlView(View):
    def create_html(self):
        raise NotImplementedError("You have to implement `create_html` method")

    @property
    def widget(self):
        webview = QtWebKit.QWebView()
        webview.setHtml(self.create_html())
        return webview