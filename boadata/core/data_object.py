# from .data_properties import DataProperties
from collections import OrderedDict
import odo            # Make optional?
import blinker


class DataObject(object):
    '''A basic object that contains data representable by boadata.

    :type registered_types: OrderedDict[str, type]
    :type real_type: type | None
    :type type_name: str

    Typically, some of the nodes have data objects,
    An object can have multiple representations (like numpy array, etc.)
    '''
    def __init__(self, inner_data=None, uri=None, source=None, **kwargs):
        if self.real_type and not isinstance(inner_data, self.real_type):
            raise RuntimeError("Invalid type of inner data.")
        self.inner_data = inner_data
        self.uri = uri
        self.source = source
        # self.custom_conversions = []

    registered_types = OrderedDict()

    changed = blinker.Signal("changed")    # For dynamic data objects

    @staticmethod
    def register_type(boadata_type):     # TODO: Perhaps this could be in some kind of metaclass?
        DataObject.registered_types[boadata_type.type_name] = boadata_type
        return boadata_type

    real_type = None

    type_name = None

    # type_description = "Unknown type"

    def _odo_convert(self, new_type_name):
        new_type = DataObject.registered_types[new_type_name]
        if not new_type:
            raise RuntimeError("Data type {0} does not exist.".format(new_type_name))
        new_real_type = new_type
        if not new_real_type:
            raise RuntimeError("One of the types for odo conversion is not defined.")
        new_inner_data = odo.convert(self.inner_data, new_real_type)
        return new_type(inner_data=new_inner_data, source=self)

    @classmethod
    def _is_odo_convertible(self, new_type_name):
        new_type = DataObject.registered_types[new_type_name]
        return bool(odo.convert.path(self.real_type, new_type.real_type))

    @classmethod
    def accepts_uri(cls, uri):
        """

        :type uri: str
        """
        return False

    @classmethod
    def from_uri(cls, uri, **kwargs):
        """"Create an object of this class from an URI.

        :param uri: URI in the odo sense
        :type uri: str
        """
        if cls == DataObject:
            for type_ in DataObject.registered_types.values():
                if type_.accepts_uri(uri):
                    return type_.from_uri(uri, **kwargs)
        else:
            inner_data = odo.odo(uri, cls.real_type)
            return cls(inner_data=inner_data, **kwargs)

    # @staticmethod
    # def from_object(object_):
    #     for type_ in DataObject.registered_types.values():
    #         if isinstance(object_, type_.real_type):
    #             return  type_(inner_data=object_)
    #     return None

    def is_convertible_to(self, new_type_name):
        """

        :type new_type_name: str
        :rtype: bool
        """
        return self.__class__._is_odo_convertible(new_type_name)

    def convert(self, new_type_name, **kwargs):
        """Convert to another boadata-supported type.

        :type new_type_name: str
        :rtype DataObject

        Auto-conversion returns the same object.
        """
        if new_type_name == self.type_name:
            return self
        return self._odo_convert(new_type_name, **kwargs)


    # @property
    # def title(self):
    #     return str(self)

    # @property
    # def properties(self):
    #     return DataProperties()

    @property
    def shape(self):
        """Shape of the data.

        :rtype: tuple(int)
        """
        return ()

    @property
    def ndim(self):
        """Dimensionality of the data.

        :rtype: int
        """
        return 0

    @property
    def columns(self):
        """Column names.

        :rtype: list[str] | None
        """
        if hasattr(self.inner_data, "columns"):
            return list(self.inner_data.columns.values)
        else:
            return None