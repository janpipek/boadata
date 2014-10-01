from view import View, register_view
import pyqtgraph as pg

class XYPlotView(View):
	title = "XY Plot"

	@classmethod
	def supported_types(cls):
		return ("xy",)

	@property
	def widget(self):
		x, y = self.data_object.to("xy")
		pw = pg.PlotWidget()
		pw.plot(x, y)
		return pw

register_view(XYPlotView)