# from .data_properties import DataProperties
from collections import OrderedDict
import odo            # Make optional?
import blinker
from .data_conversion import DataConversion, ConversionUnknown


class DataObject(object):
    '''A basic object that contains data representable by boadata.

    :type registered_types: OrderedDict[str, type]
    :type real_type: type | None
    :type type_name: str

    It is necessary to keep all arguments keyword (enforceable in Python 3).
    '''
    def __init__(self, inner_data=None, uri=None, source=None, **kwargs):
        if self.real_type and not isinstance(inner_data, self.real_type):
            raise RuntimeError("Invalid type of inner data: `{0}` instead of expected `{1}`".format(
                inner_data.__class__.__name__, self.real_type.__name__
            ))
        self.inner_data = inner_data
        self.uri = uri
        self.source = source

    registered_types = OrderedDict()

    registered_default_types = {}

    changed = blinker.Signal("changed")    # For dynamic data objects

    @staticmethod
    def register_type(default=False):
        """Decorator that registers the data type

        :param default: Whether to serve as DataObject.from_native handler
           for the real type of the data object.
        :return:

        Automatically discovers conversion in the form of __to_type__ and __from_type__
        (see DataConversion.discover)
        """
        if isinstance(default, type):
            raise RuntimeError("Invalid use of decorator. Please, use DataObject.register_type() ")
        def wrap(boadata_type):
            DataObject.registered_types[boadata_type.type_name] = boadata_type
            DataConversion.discover(boadata_type)
            if default:
                DataObject.registered_default_types[boadata_type.real_type] = boadata_type
            boadata_type._registered = True
            return boadata_type
        return wrap

    real_type = None

    type_name = None

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
        
        This method can be (but needn't be) overridden in daughter classes:
        By default, it uses odo to import the data.

        When called as DataObject.from_uri, it first tries to find an appropriate class
        by checking all registered types.
        """
        if cls == DataObject:
            for type_ in DataObject.registered_types.values():
                if type_.accepts_uri(uri):
                    return type_.from_uri(uri, **kwargs)
            raise BaseException("Cannot interpret " + uri + ".")
        else:
            inner_data = odo.odo(uri, cls.real_type, **kwargs)
            return cls(inner_data=inner_data, uri=uri, **kwargs)

    @classmethod
    def from_native(cls, native_object, **kwargs):
        """

        :param native_object:
        :param kwargs:
        :return:

        Is idempotent
        """
        if cls == DataObject:
            if isinstance(native_object, DataObject):
                return native_object
            boadata_type = DataObject.registered_default_types.get(type(native_object))
            if not boadata_type:
                raise RuntimeError("Native object of the type {0} not understood.".format(type(native_object).__name__))
            return boadata_type.from_native(native_object, **kwargs)
        else:
            if isinstance(native_object, DataObject):
                return native_object.convert(cls.type_name, **kwargs)
            return cls(inner_data=native_object, **kwargs)

    def is_convertible_to(self, new_type_name):
        """

        :type new_type_name: str | type
        :rtype: bool
        """
        if isinstance(new_type_name, type):
            new_type, new_type_name = new_type_name, new_type_name.type_name
        else:
            if not new_type_name in DataObject.registered_types:
                return False
            new_type = DataObject.registered_types[new_type_name]
        if isinstance(self, new_type):
            return True
        if not (self.type_name, new_type_name) in DataConversion.registered_conversions:
            return False
        conversion = DataConversion.registered_conversions[(self.type_name, new_type_name)]
        return conversion.applies(self)

    @classmethod
    def is_convertible_from(cls, data_object):
        return data_object.is_convertible_to(cls)

    @property
    def allowed_conversions(self):
        return [ key for (key, conversion) in DataConversion.registered_conversions.items() if key[0] == self.type_name and conversion.applies(self, key[1])]

    def convert(self, new_type_name, **kwargs):
        """Convert to another boadata-supported type.

        :type new_type_name: str
        :rtype DataObject

        Auto-conversion returns the same object.
        Default implementation is based on odo.
        """
        # TODO: check argument?

        new_type = DataObject.registered_types[new_type_name]
        if isinstance(self, new_type):
            return self
        conversion = DataConversion.registered_conversions.get((self.__class__.type_name, new_type_name))
        if not conversion:
            raise ConversionUnknown("Unknown conversion from {0} to {1}".format(self.__class__.type_name, new_type_name))
        return conversion.convert(self, new_type, **kwargs)

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
        
        Example: Shape of the 4x3 matrix is (4, 3)
        """
        if hasattr(self.inner_data, "shape"):
            return tuple(self.inner_data.shape)
        return ()

    @property
    def ndim(self):
        """Dimensionality of the data.

        :rtype: int
        
        Example: A 4x3 matrix has dimensionality 2.
        """
        if hasattr(self.inner_data, "ndim"):
            return int(self.inner_data.ndim)
        else:
            return len(self.shape)

    @property
    def dtype(self):
        if hasattr(self.inner_data, "dshape"):
            return self.inner_data.dshape
        else:
            return None

    @property
    def columns(self):
        """Column names (in multidimensional mappings, the value variables)

        :rtype: list[str] | None
        
        Default variant understands pandas DataFrames
        """
        if hasattr(self.inner_data, "columns"):
            return list(self.inner_data.columns.values)
        else:
            return None

    @staticmethod
    def proxy_methods(methods, wrap=True, same_class=False, through=None):
        """Decorator which ....

        It is not possible to proxy slots!
        """
        def wrapper(boadata_type):
            if isinstance(methods, str):
                method_names = [methods]
            else:
                method_names = methods
            for method_name in method_names:
                def proxied_method(self, *args, **kwargs):
                    if through:
                        native_method = getattr(self.convert(through), method_name)
                    else:
                        native_method = getattr(self.inner_data, method_name)
                    result = native_method(*args, **kwargs)
                    if not wrap:
                        return result
                    elif same_class:
                        return boadata_type.from_native(result)
                    else:
                        return DataObject.from_native(result)
                setattr(boadata_type, method_name, proxied_method)
            return boadata_type
        return wrapper

    def evaluate(self, expression):
        """Do calculation on columns of the dataset.

        :param expression: a valid expression
        :type expression: string
        :return: boadata.data.NumpyArray

        Based on numexpr library
        """
        import numexpr as ne
        import numpy as np
        local_dict = {
            col : self[col].inner_data for col in self.columns if isinstance(col, str)
        }
        global_dict = {
            "nan" : np.nan,
            "inf" : np.inf
        }
        result = ne.evaluate(expression, local_dict=local_dict, global_dict=global_dict)
        array_type = DataObject.registered_types["numpy_array"]
        return array_type(inner_data=result)

class OdoDataObject(DataObject):
    def __init__(self, uri, **kwargs):
        inner_data = odo.resource(uri)
        super(OdoDataObject, self).__init__(inner_data=inner_data, uri=uri, **kwargs)

    @classmethod
    def from_uri(cls, uri, **kwargs):
        return cls(uri=uri, **kwargs)