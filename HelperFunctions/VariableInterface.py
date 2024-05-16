class VariableInterfaceMeta(type):
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return (hasattr(subclass, 'get_value') and
                callable(subclass.get) and
                hasattr(subclass, 'set_value') and
                callable(subclass.set))


class VariableInterface(metaclass=VariableInterfaceMeta):

    @staticmethod
    def get_value(self):
        pass
    def set_value(self, value):
        pass

