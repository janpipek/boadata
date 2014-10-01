from PyQt4.QtGui import QTableWidget

class PropertyView(object):
	def __init__(self, data_object):
		self.data_object = data_object
		self.props = data_object.properties

	def create_table(self, props):
		table = QTableWidget()
		return table

	def show(self):
		if hasattr(self.props, "keys"):
			props = self.props
			tabs = True
		else:
			tabs = False
		table = self.create_table(self.props)
		table.show()
