import HelperFunctions.Constants as Constants
from HighLevelControls.Parser import ParsedMessage
from HighLevelControls.Controller import Controller
from HelperFunctions.Exceptions import catch_error_helper
from HighLevelControls.Managers.LoggingManager import LoggingManager
from HighLevelControls.Managers.NotificationManager import NotificationManager

class ShutDownManager:


    commands = {
                 Constants.ACTION_SHUTDOWN: Controller.shutdown,
                 Constants.ACTION_CANCEL_SHUTDOWN: Controller.cancel_shutdown
               }

    @staticmethod
    def process_message(parsed_message):
        LoggingManager.log_info("ShutDownManager.process_message(): Executing")
        try:
            for device, method_key in parsed_message.dictionary.items():
                if method_key in ShutDownManager.commands:
                    method = ShutDownManager.commands.get(method_key)
                    ShutDownManager._execute_command(method, device)

                else:
                    LoggingManager.log_error(f"ShutDownManager.process_message(): Invalid Command Recieved {device}: {message}")

            LoggingManager.log_info("ShutDownManager.process_message(): Exiting")
            parsed_messages = ParsedMessage(Constants.MQTT_TOPIC_NOTIFICATIONS, {"CONTROLLER_CURRENT_VALUES":""})
            NotificationManager.process_message(parsed_messages)

        except Exception as e:
            LoggingManager.log_error(f'ShutDownManager.process_message(): Error! {e}')
            catch_error_helper(e)


    @staticmethod
    def _execute_command(method, qualifier):
        LoggingManager.log_info("ShutDownManager._execute_command(): Executing")
        if qualifier != "\"\"":
            method(qualifier)
        else:
            method()
        LoggingManager.log_info("ShutDownManager._execute_command(): Exiting")
