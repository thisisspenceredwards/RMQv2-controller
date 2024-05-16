import json
import HelperFunctions.Constants as Constants
from HelperFunctions.Exceptions import HighLevelException
from HighLevelControls.Managers.LoggingManager import LoggingManager
from HighLevelControls.Managers.ConstantsManager import ConstantsManager
class NotificationManager:


    _channel = None
    _connection = None


    @staticmethod
    def setup_connection(connection):
        LoggingManager.log_info("NotificationManager.setup_connection(): Executing")
        if connection:
            NotificationManager._connection = connection
            NotificationManager._channel = connection.channel()
        LoggingManager.log_info("NotificationManager.setup_connection(): Exiting")


    @staticmethod
    def process_message(parsed_messages):
        LoggingManager.log_info("NotificationManager.parse_message(): Executing")
        commands = parsed_messages.dictionary

        methods = {
                    Constants.CONTROLLER_CURRENT_VALUES: NotificationManager._controller_current_values,
                     Constants.SETTINGS_CURRENT_VALUES: NotificationManager._settings_current_values,
                      Constants.SWEEP_CURRENT_VALUES: NotificationManager._sweep_current_values,
                       Constants.CONTROLLER_LOG: NotificationManager._controller_log
                   }


        try:
            for function, message in commands.items():
                message = message.upper() if message else None
                if function in methods:
                    methods.get(function)(message)
                    LoggingManager.log_info("NotificationManager.process_message(): Successful")
                else:
                    LoggingManager.log_info(f"NotificationManager.process_message(): Invalid Message {message} {function}")

        except Exception as e:
            LoggingManager.log_error("NotificationManager.process_message(): Failure: " + str(e))
            raise HighLevelException(class_name = "NotificationManager", function_name = "process_messsage", message = "Channel may be closed", error = e)

        LoggingManager.log_info("NotificationManager.process_message(): Exiting")


    @staticmethod
    def _controller_current_values(message = None):
         LoggingManager.log_info("NotificationManager.controller_current_values(): Executing")
         message = ConstantsManager.getInstance().current_values()
         NotificationManager._channel.basic_publish(exchange = Constants.CLIENT_EXCHANGE, routing_key = '', body = message)
         LoggingManager.log_info("NotificationManager.controller_current_values(): Exiting")


    @staticmethod
    def _settings_current_values(message = None):
         LoggingManager.log_info("NotificationManager.settings_current_values(): Executing")
         message = ConstantsManager.getInstance().settings_current_values()
         NotificationManager._channel.basic_publish(exchange = Constants.CLIENT_EXCHANGE, routing_key = '', body = message)
         LoggingManager.log_info("NotificationManager.settings_current_values(): Exiting")


    @staticmethod
    def _controller_log(message = None):
        LoggingManager.log_info("NotificationManager.controller_log(): Executing")
        with open('app.log', 'r') as file:
            log = ""
            for line in reversed(list(file)):
                log += line
            log_dict = {"LOG": log}
            log_json = json.dumps(log_dict)
            NotificationManager._channel.basic_publish(exchange = Constants.CLIENT_EXCHANGE, routing_key = '', body = log_json)
        LoggingManager.log_info("NotificationManager.controller_log(): Exiting")


    @staticmethod
    def _sweep_current_values(message = None):
        LoggingManager.log_info("NotificationManager._sweep_current_values(): Executing")
        message = ConstantsManager.getInstance().sweep_current_values()
        NotificationManager._channel.basic_publish(exchange = Constants.CLIENT_EXCHANGE, routing_key = '', body = message)
        LoggingManager.log_info("NotificationManager.sweep_current_values(): Exiting")

