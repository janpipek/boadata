from qtpy import QtWebKit, QtCore


class WebkitBackend(object):
    @classmethod
    def create_widget(self, html=None, uri=None):
        webview = QtWebKit.QWebView()
        if html:
            webview.setHtml(html)
        elif uri:
            url = QtCore.QUrl(uri)
            webview.setUrl(url)
        return webview
