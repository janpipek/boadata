# from .data_properties import DataProperties
from collections import OrderedDict
import odo            # Make optional?
import blinker
import weakref
from .data_conversion import DataConversion, ConversionUnknown


class _DataObjectRegistry():
    registered_types = OrderedDict()

    registered_default_types = {}

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


class _DataObjectConversions():
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
            last_exception = None
            for type_ in DataObject.registered_types.values():
                if type_.accepts_uri(uri):
                    try:
                        return type_.from_uri(uri, **kwargs)
                    except Exception as exc:
                        last_exception = exc
            if last_exception:
                raise last_exception
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
                raise RuntimeError("Native object of the type {0} not understood.".format(type(native_object)))
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
        return [ key for (key, conversion) in DataConversion.registered_conversions.items() if key[0] == self.type_name and conversion.applies(self)]

    def convert(self, new_type_name=None, **kwargs):
        """Convert to another boadata-supported type.

        :type new_type_name: str
        :rtype DataObject

        Auto-conversion returns the same object.
        Default implementation is based on odo.
        """
        if new_type_name is None:
            available = [key[1] for key in DataConversion.registered_conversions.keys() if key[0] == self.__class__.type_name]
            raise TypeError("convert() missing 1 required positional argument: 'new_type_name', available argument values: {0}".format(", ".join(available)))
        # TODO: check argument?

        new_type = DataObject.registered_types[new_type_name]
        if isinstance(self, new_type):
            return self
        conversion = DataConversion.registered_conversions.get((self.__class__.type_name, new_type_name))
        if not conversion:
            available = [key[1] for key in DataConversion.registered_conversions.keys() if key[0] == self.__class__.type_name]
            raise ConversionUnknown("Unknown conversion from {0} to {1}. Available: {2}".format(self.__class__.type_name, new_type_name, ", ".join(available)))
        return conversion.convert(self, new_type, **kwargs)


class _DataObjectInterface():
    """

    Possible methods:
    - add_column(key, expression, **kwargs) - based on evaluate
    -
    """
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
    def size(self):
        if hasattr(self.inner_data, "size"):
            return int(self.inner_data.size)
        else:
            from operator import mul
            from functools import reduce
            reduce(mul, self.shape, 1)

    @property
    def dtype(self):
        if hasattr(self.inner_data, "dtype"):
            return self.inner_data.dtype
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

    @property
    def name(self):
        """

        :rtype: str | None
        """
        if hasattr(self.inner_data, "name"):
            return self.inner_data.name
        else:
            return None


class DataObject(_DataObjectRegistry, _DataObjectConversions, _DataObjectInterface):
    '''A basic object that contains data representable by boadata.

    :type registered_types: OrderedDict[str, type]
    :type real_type: type | None
    :type type_name: str
    :param source: From where we obtained the object (kept as weak reference)

    It is necessary to keep all arguments keyword (enforceable in Python 3).
    '''
    def __init__(self, inner_data=None, uri=None, source=None, **kwargs):
        if self.real_type and not isinstance(inner_data, self.real_type):
            raise RuntimeError("Invalid type of inner data: `{0}` instead of expected `{1}`".format(
                inner_data.__class__.__name__, self.real_type.__name__
            ))
        self.inner_data = inner_data
        self.uri = uri
        if source:
            self.source = weakref.ref(source)

    changed = blinker.Signal("changed")    # For dynamic data objects

    real_type = None

    type_name = None

    @property
    def title(self):
        return repr(self)

    def __repr__(self):
        return "{0}(\"{1}\")".format(self.__class__.__name__, self.uri)

    @staticmethod
    def proxy_methods(methods, wrap=True, unwrap_args=True, same_class=True, through=None):
        """Decorator to apply on DataObject descendants.

        :param wrap: Whether to wrap result
        :param unwrap_args: Whether to unwrap arguments
        :param same_class: Whether to try to convert to self's class
        :param through: if None, done via inner_data, otherwise through a named type

        It is not possible to proxy slots, but it is possible to inherit proxied slots :-)
        """
        import boadata
        def wrapper(boadata_type):
            if isinstance(methods, str):
                method_names = [methods]
            else:
                method_names = methods

            def make_method(method_name):
                def proxied_method(self, *args, **kwargs):
                    if unwrap_args:
                        args = [boadata.unwrap(arg) for arg in args]
                        kwargs = {key: boadata.unwrap(value) for key, value in kwargs.items()}

                    if through:
                        native_method = getattr(self.convert(through), method_name)
                    else:
                        native_method = getattr(self.inner_data, method_name)
                    result = native_method(*args, **kwargs)
                    if not wrap:
                        return result
                    elif same_class and isinstance(result, self.real_type):
                        return self.__class__.from_native(result)
                    else:
                        try:
                            return DataObject.from_native(result)
                        except:
                            return result
                return proxied_method
            for method_name in method_names:
                setattr(boadata_type, method_name, make_method(method_name))
            return boadata_type
        return wrapper

    def evaluate(self, expression, wrap=True):
        """Do calculation on columns of the dataset.

        :param expression: a valid expression
        :type expression: string

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
        if wrap:
            return DataObject.from_native(result, source=self)
        else:
            return result

    def where(self, condition, sql=False):
        """Choose a subset of a dataset.

        :param condition: a valid condition returning boolean
        :param sql: if True, the condition is evaluated as sql WHERE clause
        """
        if sql:
            if not "sql" in dir(self):
                raise RuntimeError("Object {0} does not support SQL.".format(self.__class__.__name__))
            query = "SELECT * FROM data WHERE {0}".format(condition)
            return self.sql(query, table_name="data")
        else:    
            # TODO: Allow to be lambda
            import numpy as np
            if not self.size:
                mask = []
            else:
                mask = self.evaluate(condition, wrap=False)
                if mask.dtype != np.dtype(bool):
                    raise RuntimeError("The result of condition has to be a boolean array")
            return DataObject.from_native(self.inner_data[mask], source=self)

    def apply_native(self, method_name, *args, **kwargs):
        """Apply a method defined on the native object.

        If possible, converts the result to DataObject.
        """
        # TODO: Check that it is ok (see proxy etc., consider a clever proxy attribute)
        method = getattr(self.inner_data, method_name)
        result = method(*args, **kwargs)
        try:
            result = DataObject.from_native(result)
        except:
            pass
        return result


class OdoDataObject(DataObject):
    def __init__(self, uri, **kwargs):
        inner_data = odo.resource(uri)
        super(OdoDataObject, self).__init__(inner_data=inner_data, uri=uri, **kwargs)

    @classmethod
    def from_uri(cls, uri, **kwargs):
        return cls(uri=uri, **kwargs)