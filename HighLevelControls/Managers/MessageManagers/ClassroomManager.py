import serial
import HelperFunctions.Constants as Constants
from HighLevelControls.Controller import Controller
from HighLevelControls.Parser import ParsedMessage
from HighLevelControls.Managers.LoggingManager import LoggingManager
from HighLevelControls.Managers.NotificationManager import NotificationManager
from HighLevelControls.Managers.RelayManager import RelayManager
from HighLevelControls.Managers.BlindManager import BlindManager
from HelperFunctions.Exceptions import catch_error_helper

#Relay gets refreshed from BlindManager and BlindThread, blind thread and manager get called everytime a message is received

class ClassroomManager:


    commands = {
                 Constants.ACTION_MOVE_BLIND_TOP: lambda name: BlindManager.on_message(name, 0),
                 Constants.ACTION_MOVE_BLIND_MIDDLE: lambda name: BlindManager.on_message(name, 1),
                 Constants.ACTION_MOVE_BLIND_BOTTOM: lambda name: BlindManager.on_message(name, 2),
                 Constants.ACTION_LIGHT_ON: lambda name: Controller.light_on(name),
                 Constants.ACTION_LIGHT_OFF: lambda name: Controller.light_off(name),
                 Constants.ACTION_RECEPTACLE_ON: lambda name: Controller.receptacle_on(name),
                 Constants.ACTION_RECEPTACLE_OFF: lambda name: Controller.receptacle_off(name)
               }

    @staticmethod
    def process_message(parsed_message):
        LoggingManager.log_info("ClassroomManager.process_message(): Executing")
        try:
            RelayManager.getInstance() #renews the connection to the usb board and does validation
            for device, method_key in parsed_message.dictionary.items():
                if method_key in ClassroomManager.commands:
                    method = ClassroomManager.commands.get(method_key)
                    ClassroomManager._execute_command(method, device)

                else:
                    LoggingManager.log_error(f"ClassroomManager.process_message(): Invalid Command Recieved {device}, {method_key}")

            LoggingManager.log_info("ClassroomManager.process_message(): Exiting")
            BlindManager.start()
            parsed_messages = ParsedMessage(Constants.MQTT_TOPIC_NOTIFICATIONS, {"CONTROLLER_CURRENT_VALUES":""})
            NotificationManager.process_message(parsed_messages)

        except serial.SerialException as e:
            RelayManager.close_connection()
            LoggingManager.log_error(f'ClassroomManager.process_message(): Error! {e}')

        except Exception as e:
            LoggingManager.log_error(f'ClassroomManager.process_message(): Error! {e}')
            catch_error_helper(e)

        #Batch all blind manager related commands so they stay in sync


    @staticmethod
    def _execute_command(method, qualifier):
        LoggingManager.log_info("ClassroomManager._execute_command(): Executing")
        if qualifier != "\"\"":
            method(qualifier)
        else:
            method()
        LoggingManager.log_info("ClassroomManager._execute_command(): Exiting")

