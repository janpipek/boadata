from collections import OrderedDict
import odo


class DataConversion(object):
    def __init__(self, type_name1, type_name2, method=None, condition=None):
        # Unify arguments
        if isinstance(type_name1, type):
            type_name1 = type_name1.type_name
        if isinstance(type_name2, type):
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

    def convert(self, origin, check=True, **kwargs):
        if check and not self.applies(origin):
            raise RuntimeError("Cannot convert to " + self.type_name2)
        return self._convert(origin, **kwargs)

    def _convert(self, origin, **kwargs):
        return self.method(origin, **kwargs)

    @staticmethod
    def register(type1, type2):
        def wrap(method):
            conversion = DataConversion(type1, type2, method)
            conversion._register()
            return method
        return wrap

    @classmethod
    def enable_to(cls, type2, condition=None):
        def wrap(type1):
            conversion = cls(type1, type2, condition)
            conversion._register()
            return type1
        return wrap

    @classmethod
    def enable_from(cls, type1, condition=None):
        def wrap(type2):
            conversion = cls(type1, type2, condition)
            conversion._register()
            return type2
        return wrap


class OdoConversion(DataConversion):
    def __init__(self, type_name1, type_name2, condition=None):
        super(OdoConversion, self).__init__(type_name1=type_name1, type_name2=type_name2, condition=condition)

        from . import DataObject
        if isinstance(type_name1, type):
            self.type1 = type_name1
        else:
            self.type1 = DataObject.registered_types[type_name1]
        if isinstance(type_name2, type):
            self.type2 = type_name2
        else:
            self.type2 = DataObject.registered_types[type_name2]

        if (self.type1.real_type != self.type2.real_type) and not bool(odo.convert.path(self.type1.real_type, self.type2.real_type)):
            raise RuntimeError("Odo cannot convert the types {0} and {1}.".format(self.type1.real_type.__name__, self.type2.real_type.__name__))

    def _convert(self, origin, **kwargs):
        new_inner_data = odo.convert(origin.inner_data, self.type2.real_type, **kwargs)
        return self.type2(inner_data=new_inner_data, source=origin)


class IdentityConversion(DataConversion):
    def __init__(self, type_name1, type_name2, condition = None):
        super(IdentityConversion, self).__init__(type_name1=type_name1, type_name2=type_name2, condition=condition)

    def _convert(self, origin, **kwargs):
        from . import DataObject
        type2 = DataObject.registered_types[self.type_name2]
        new_inner_data = origin.inner_data
        return type2(inner_data=new_inner_data, source=origin)
