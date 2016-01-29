from .data_node import DataNode
import logging


class DataSource(DataNode):
    def has_object(self):
        return True

    @property
    def data_object(self):
        if self._data_object is None:
            self._data_object = self.create_data_object()
            logging.debug("Data object created from node %s." % self.title)
        return self._data_object