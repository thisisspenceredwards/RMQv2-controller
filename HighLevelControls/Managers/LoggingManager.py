import logging
from logging.handlers import RotatingFileHandler

class LoggingManager:

    _app_log = None

    @staticmethod
    def _initialize():
        if LoggingManager._app_log is None:
            LoggingManager._app_log = logging.getLogger('CSILogger')
            LoggingManager._app_log.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            my_handler = RotatingFileHandler('app.log', mode = 'a', maxBytes = 1*1024*1024, backupCount = 5)
            my_handler.setFormatter(formatter)
            my_handler.setLevel(logging.INFO)
            LoggingManager._app_log.addHandler(my_handler)


    @staticmethod
    def log_info(message):
        LoggingManager._initialize()
        print(message)
        LoggingManager._app_log.info(message)


    @staticmethod
    def log_warn(message):
        LoggingManager._initialize()
        print(message)
        LoggingManager._app_log.warn(message)


    @staticmethod
    def log_error(message):
        LoggingManager._initialize()
        print(message)
        LoggingManager._app_log.error(message)


    @staticmethod
    def log_critical(message):
        LoggingManager._initialize()
        print(message)
        LoggingManager._app_log.critical(message)
