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

    It is necessary to keep all arguments keyword (enforceable in Python 3)
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

    def _odo_convert(self, new_type, **kwargs):
        if not new_type:
            raise RuntimeError("Data type {0} does not exist.".format(new_type_name))
        new_real_type = new_type.real_type
        if not new_real_type:
            raise RuntimeError("One of the types for odo conversion is not defined.")
        # print(type(self.inner_data), new_real_type)
        if isinstance(self.inner_data, new_real_type):
            new_inner_data = self.inner_data    # Clone?
        else:
            print("Converting {0} to {1}".format(type(self.inner_data), new_real_type))
            new_inner_data = odo.convert(self.inner_data, new_real_type, **kwargs)
        return new_type(inner_data=new_inner_data, source=self)

    @classmethod
    def _is_odo_convertible(self, new_type):
        try:
            return bool(odo.convert.path(self.real_type, new_type.real_type))
        except:
            return False

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
            raise BaseException("Cannot interpret " + uri + ".")
        else:
            inner_data = odo.odo(uri, cls.real_type)
            return cls(inner_data=inner_data, uri=uri, **kwargs)

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
        new_type = DataObject.registered_types[new_type_name]
        if isinstance(self, new_type):
            return True
        if isinstance(self.inner_data, new_type.real_type):
            return True
        return self.__class__._is_odo_convertible(new_type)

    def convert(self, new_type_name, **kwargs):
        """Convert to another boadata-supported type.

        :type new_type_name: str
        :rtype DataObject

        Auto-conversion returns the same object.
        """
        new_type = DataObject.registered_types[new_type_name]
        if isinstance(self, new_type):
            return self
        return self._odo_convert(new_type, **kwargs)


    @property
    def title(self):
        return repr(self)

    def __repr__(self):
        return "{0}(\"{1}\")".format(self.__class__.__name__, self.uri)

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