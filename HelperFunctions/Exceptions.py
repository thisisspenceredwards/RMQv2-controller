class CustomError(Exception):
    pass



#convienence exception
class LocalException(CustomError):
    def __init__(self, class_name, function_name, message, error = None):
        self.error = error
        self.message = message
        self.class_name = class_name
        self.function_name = function_name
        super().__init__(self.message)


    def __str__(self):
        return f"{self.class_name} -> {self.function_name}: {self.message} {self.error or ''}"


#This exception should only be caught by the top level try/catch and should need to reinitialize the whole app e.g. rabbitmq connection has closed erroneously
class HighLevelException(CustomError):
    def __init__(self, class_name, function_name, message, error = None):
        self.error = error
        self.message = message
        self.class_name = class_name
        self.function_name = function_name
        super().__init__(self.message)


    def __str__(self):
        return f"{self.class_name} -> {self.function_name}: {self.message} {self.error or ''}"


def catch_error_helper(error):
    if not isinstance(error, LocalException):
        raise error
