from .view import View


# @View.register_view
class PlotView(View):
    def accepts(cls, data_object):
        if data_object.ndim == 2 and (data_object.shape[0] == 2 or data_object.shape[1] == 2):
            return True
        return False

    def create_widget(self):
        pass
