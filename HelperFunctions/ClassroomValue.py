from HelperFunctions.VariableInterface import VariableInterface

class ClassroomValue(VariableInterface):

    def __init__(self, value, cast_to_type):
        self._value = value
        self.cast_to_type = cast_to_type

    def get_value(self):
        return self._value

    def set_value(self, value):
        try:
            self._value = self.cast_to_type(value)
        except Exception as e:
            raise ValueException("Unable to cast to appropriate type")

    def del_value(self):
        del self._value

    value = property(get_value, set_value, del_value)

