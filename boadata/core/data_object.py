# from .data_properties import DataProperties
from collections import OrderedDict
import odo            # Make optional?


class DataObject(object):
    '''A basic object that contains data representable by boadata.

    Typically, some of the nodes have data objects,
    An object can have multiple representations (like numpy array, etc.)
    '''
    def __init__(self, inner_data=None, source=None):
        if self.real_type and not isinstance(inner_data, self.real_type):
            raise RuntimeError("Invalid type of inner data.")
        self.inner_data = inner_data
        self.source = source

    registered_types = OrderedDict()

    @staticmethod
    def register_type(boadata_type):     # TODO: Perhaps this could be in some kind of metaclass?
        DataObject.registered_types[boadata_type.name] = boadata_type
        return boadata_type

    real_type = None

    name = None

    def _odo_convert(self, new_type_name):
        new_type = DataObject.registered_types[new_type_name]
        if new_type == self.__class__:
            return self
        new_real_type = new_type
        if not new_real_type:
            raise RuntimeError("One of the types for odo conversion is not defined.")
        new_inner_data = odo.convert(self.inner_data, new_real_type)
        return new_type(inner_data=new_inner_data, source=self)

    @classmethod
    def from_uri(cls, uri):
        """"Create an object of this class from an URI.

        :param uri: URI in the odo sense
        :type uri: str
        """
        inner_data = odo.odo(uri, cls.real_type)
        return cls(inner_data=inner_data)

    # @property
    # def title(self):
    #     return str(self)

    # @property
    # def properties(self):
    #     return DataProperties()

    # TODO: Give this some meaning
    # read_only = True

    # @property
    # def conversions(self):
    #     '''Available object conversions.
    #
    #     It is possible to override this property if conversion list is not static.
    #     '''
    #     return tuple(attr.partition("_")[2] for attr in dir(self) if attr.startswith("as_"))
    #
    # def to(self, conversion):
    #     '''Perform the conversion.
    #     '''
    #     attr = 'as_' + conversion
    #     if not hasattr(self, attr):
    #         raise RuntimeError("Conversion not supported.")
    #     return getattr(self, attr)()
    #
    # def converts_to(self, format):
    #     '''Whether the object can be represented as a format.
    #
    #     :param format: name of the type (like numpy_array, pandas_frame, ...)
    #     '''
    #     return format in self.conversions

    @property
    def shape(self):
        return None

    @property
    def ndim(self):
        return None
    #
    # @property
    # def columns(self):
    #     return None