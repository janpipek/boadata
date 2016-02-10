from collections import OrderedDict
import odo


class DataConversion(object):
    def __init__(self, type1, type2, method, condition=None):
        self.type1 = type1
        self.type2 = type2
        self.method = method
        self.condition = condition

    registered_conversions = OrderedDict()

    def applies(self, origin, target_type):
        if not isinstance(origin, self.type1):
            return False
        if not isinstance(target_type == self.type2):
            return False
        if not self.condition or not self.condition(origin):
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
            raise RuntimeError("Cannot convert to " + self.type2.name)
        return self._convert(origin, **kwargs)

    def _convert(self, origin, **kwargs):
        return self.method(origin, **kwargs)

    @staticmethod
    def register(type1, type2):
        def wrap(method):
            conversion = DataConversion(type1, type2, method)
            DataConversion.registered_conversions.append((type1, type2), conversion)
            return method
        return wrap


class OdoConversion(DataConversion):
    def __init__(self, type1, type2):
        self.type1 = type1
        self.type2 = type2
        if not bool(odo.convert.path(type1.real_type, type2.real_type)):
            raise RuntimeError("Odo cannot convert the types {0} and {1}.".format(type1.real_type.__name__, type2.real_type.__name__))

    def _convert(self, origin, **kwargs):
        new_inner_data = odo.convert(origin.inner_data, self.type2.real_type, **kwargs)
        return self.type2(inner_data=new_inner_data, source=origin)

    @staticmethod
    def enable_to(type2):
        def wrap(type1):
            conversion = OdoConversion(type1, type2)
            DataConversion.registered_conversions.append((type1, type2), conversion)
            return type1
        return wrap

    @staticmethod
    def enable_from(type1):
        def wrap(type2):
            conversion = OdoConversion(type1, type2)
            DataConversion.registered_conversions.append((type1, type2), conversion)
            return type1
        return wrap
