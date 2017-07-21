from collections import OrderedDict
import odo


class ConversionUnknown(RuntimeError):
    pass


class ConversionConditionFailed(RuntimeError):
    pass


class DataConversion(object):
    """

    :type _type1: type
    :type type_name1: str
    :type _type2: type
    :type type_name2: str

    """

    def __init__(self, type_name1, type_name2, method=None, condition=None):
        self._type1 = None
        self._type2 = None

        # Unify arguments
        if isinstance(type_name1, type):
            self._type1 = type_name1
            type_name1 = type_name1.type_name
        if isinstance(type_name2, type):
            self._type2 = type_name2
            type_name2 = type_name2.type_name

        self.type_name1 = type_name1
        self.type_name2 = type_name2

        self.method = method
        self.condition = condition

    registered_conversions = OrderedDict()

    def _register(self):
        DataConversion.registered_conversions[(self.type_name1, self.type_name2)] = self

    def applies(self, origin):
        # Unify arguments
        target_type_name = self.type_name2

        # print("Conversion check: ", origin.type_name, " to ", target_type_name)

        # print("Checking against origin = ", self.type_name1)
        if origin.type_name != self.type_name1:
            return False

        # print("Checking against target = ", self.type_name2)
        if target_type_name != self.type_name2:
            return False

        if self.condition and not self.condition(origin):
            return False
        return True
    #
    # def get_required_arguments(self, data_object):
    #     """
    #
    #     :rtype: dict(str, str)
    #
    #     You can override this
    #     """
    #     return OrderedDict()

    @property
    def type1(self):
        from .data_object import DataObject
        if not self._type1:
            self._type1 = DataObject.registered_types[self.type_name1]
        return self._type1

    @property
    def type2(self):
        from .data_object import DataObject
        if not self._type2:
            self._type2 = DataObject.registered_types[self.type_name2]
        return self._type2

    def convert(self, origin, check=True, **kwargs):
        if check and not self.applies(origin):
            raise ConversionConditionFailed("Cannot convert to " + self.type_name2)
        return self._convert(origin, **kwargs)

    def _convert(self, origin, **kwargs):
        return self.method(origin, **kwargs)

    @staticmethod
    def register(type1, type2, condition=None):
        def wrap(method):
            conversion = DataConversion(type1, type2, method=method, condition=condition)
            conversion._register()
            return method
        return wrap

    @staticmethod
    def condition(cond):
        def wrap(method):
            method.condition = cond
            return method
        return wrap

    @staticmethod
    def discover(cls):
        for key in dir(cls):
            if key.startswith("__to_") and key.endswith("__"):
                other_type = key[5:-2]
                attr = getattr(cls, key)
                if hasattr(attr, "condition"):
                    condition = attr.condition
                else:
                    condition = None
                if cls.type_name != other_type:
                    DataConversion.register(cls.type_name, other_type, condition=condition)(attr)
            if key.startswith("__from_") and key.endswith("__"):
                other_type = key[7:-2]
                attr = getattr(cls, key)
                if hasattr(attr, "condition"):
                    condition = attr.condition
                else:
                    condition = None
                if cls.type_name != other_type:
                    DataConversion.register(other_type, cls.type_name, condition=condition)(attr)

    @classmethod
    def enable_to(cls, type2, condition=None, **kwargs):
        def wrap(type1):
            if hasattr(type1, "_registered"):
                raise RuntimeError("Cannot decorate already registered types with conversions.")
            kwargs["condition"] = condition
            conversion = cls(type1, type2, **kwargs)
            conversion._register()
            return type1
        return wrap

    @classmethod
    def enable_from(cls, type1, condition=None, **kwargs):
        def wrap(type2):
            kwargs["condition"] = condition
            conversion = cls(type1, type2, **kwargs)
            conversion._register()
            return type2
        return wrap


class OdoConversion(DataConversion):
    """Conversion based on odo.convert."""
    def __init__(self, type_name1, type_name2, condition=None):
        super(OdoConversion, self).__init__(type_name1=type_name1, type_name2=type_name2, condition=condition)
        if (self.type1.real_type != self.type2.real_type) and not bool(odo.convert.path(self.type1.real_type, self.type2.real_type)):
            raise RuntimeError("Odo cannot convert the types {0} and {1}.".format(self.type1.real_type.__name__, self.type2.real_type.__name__))

    def _convert(self, origin, **kwargs):
        # print("Converting {0} to {1}".format(origin.inner_data.__class__, self.type2.real_type))
        new_inner_data = odo.odo(origin.inner_data, self.type2.real_type, **kwargs)
        return self.type2(inner_data=new_inner_data, source=origin)


class ChainConversion(DataConversion):
    """Conversion that has an intermediate data type."""
    def __init__(self, type_name1, type_name2, through, condition = None, pass_kwargs=[]):
        super(ChainConversion, self).__init__(type_name1=type_name1, type_name2=type_name2, condition=condition)
        self.through = through
        self.pass_kwargs = pass_kwargs

    def _convert(self, origin, **kwargs):
        second_kwargs = {}
        for arg in self.pass_kwargs:
            second_kwargs[arg] = kwargs.pop(arg)
        intermediate = origin.convert(self.through, **kwargs)
        final = intermediate.convert(self.type_name2, **second_kwargs)
        final.source = self
        return final


class IdentityConversion(DataConversion):
    """Conversion that does not change internal data type."""
    def _convert(self, origin, **kwargs):
        return self.type2(inner_data=origin.inner_data, source=origin)


class ConstructorConversion(DataConversion):
    """Conversion that uses constructor for conversion of inner data."""
    def _convert(self, origin, **kwargs):
        new_inner_data = self.type2.real_type(origin.inner_data)
        return self.type2(inner_data=new_inner_data, source=origin)

class MethodConversion(DataConversion):
    """Conversion that uses a method of the origin class."""
    def __init__(self, type_name1, type_name2, method_name, condition = None):
        super(MethodConversion, self).__init__(type_name1=type_name1, type_name2=type_name2, condition=condition)
        self.method_name = method_name

    def _convert(self, origin, **kwargs):
        method = getattr(origin.inner_data, self.method_name)
        new_inner_data = method(**kwargs)
        return self.type2(inner_data=new_inner_data, source=origin)
