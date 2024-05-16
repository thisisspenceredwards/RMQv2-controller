import pika
import time
import serial
import datetime
import threading
from HelperFunctions.Exceptions import catch_error_helper
import HelperFunctions.Constants as Constants
from HighLevelControls.Managers.BlindManager import BlindManager
from HighLevelControls.Managers.LoggingManager import LoggingManager
from HighLevelControls.Parser import ParsedMessage
from HighLevelControls.Controller import Controller
from HighLevelControls.Managers.RelayManager import RelayManager
from HighLevelControls.Managers.ConstantsManager import ConstantsManager


class SweepWatcher(threading.Thread):

    nonlooping_commands = {
                 Constants.ACTION_MOVE_BLIND_TOP: lambda name: BlindManager.on_message(name, 0),
                 Constants.ACTION_LIGHT_OFF: lambda name: Controller.light_off(name),
                 Constants.ACTION_RECEPTACLE_OFF: lambda name: Controller.receptacle_off(name),
                           }


    ALL_OFF_DICT = {
                       Constants.BLIND_ONE_KEY: Constants.ACTION_MOVE_BLIND_TOP,
                       Constants.BLIND_TWO_KEY: Constants.ACTION_MOVE_BLIND_TOP,
                       Constants.BLIND_THREE_KEY: Constants.ACTION_MOVE_BLIND_TOP,
                       Constants.BLIND_FOUR_KEY: Constants.ACTION_MOVE_BLIND_TOP,
                       Constants.BLIND_FIVE_KEY: Constants.ACTION_MOVE_BLIND_TOP,
                       Constants.BLIND_SIX_KEY: Constants.ACTION_MOVE_BLIND_TOP,
                       Constants.BLIND_SEVEN_KEY: Constants.ACTION_MOVE_BLIND_TOP,
                       Constants.BLIND_EIGHT_KEY: Constants.ACTION_MOVE_BLIND_TOP,
                       Constants.LIGHT_ONE_KEY: Constants.ACTION_LIGHT_OFF,
                       Constants.LIGHT_TWO_KEY: Constants.ACTION_LIGHT_OFF,
                       Constants.LIGHT_THREE_KEY: Constants.ACTION_LIGHT_OFF,
                       Constants.LIGHT_FOUR_KEY: Constants.ACTION_LIGHT_OFF,
                       Constants.RECEPTACLE_ONE_KEY: Constants.ACTION_RECEPTACLE_OFF,
                       Constants.RECEPTACLE_TWO_KEY: Constants.ACTION_RECEPTACLE_OFF,
                       Constants.RECEPTACLE_THREE_KEY: Constants.ACTION_RECEPTACLE_OFF,
                       Constants.RECEPTACLE_FOUR_KEY: Constants.ACTION_RECEPTACLE_OFF,
                       Constants.RECEPTACLE_FIVE_KEY: Constants.ACTION_RECEPTACLE_OFF,
                       Constants.RECEPTACLE_SIX_KEY: Constants.ACTION_RECEPTACLE_OFF,
                       Constants.RECEPTACLE_SEVEN_KEY: Constants.ACTION_RECEPTACLE_OFF,
                       Constants.RECEPTACLE_EIGHT_KEY: Constants.ACTION_RECEPTACLE_OFF,
                   }

    _channel = None
    _connection = None

    def __init__(self, sleep_duration = 60):
        LoggingManager.log_info("SweepWatcher.init(): Called")
        threading.Thread.__init__(self)
        self.sleep_duration = sleep_duration
        self._stop_event = threading.Event()
        LoggingManager.log_info("SweepWatcher.init(): Complete")


    def run(self):
        LoggingManager.log_info("SweepWatcher.run(): Starting")
        while not self._stop_event.isSet():
            LoggingManager.log_info("SweepWatcher.run(): Executing")
            SweepWatcher._check_sweep_dict()
            time.sleep(self.sleep_duration)
        LoggingManager.log_warn("SweepWatcher.run(): Thread has been stopped")


    def stop(self):
        LoggingManager.log_info("SweepWatcher.stop(): Executing")
        self._stop_event.set()
        LoggingManager.log_info("SweepWatcher.stop(): Exiting")


    @staticmethod
    def _check_sweep_dict():
        LoggingManager.log_info("SweepWatcher._check_sweep_dict(): Executing")
        time_now = datetime.datetime.now().strftime("%H:%M")
        if time_now in Constants.SWEEP_DICT:
            try:
                RelayManager.getInstance() #renews the connection to the usb board and does validation

                parsed_message = ParsedMessage(topic = "CLASSROOM", dictionary = SweepWatcher.ALL_OFF_DICT)
                for device, method_key in parsed_message.dictionary.items():
                    if method_key in SweepWatcher.nonlooping_commands:
                        method = SweepWatcher.nonlooping_commands.get(method_key)
                        SweepWatcher._execute_command(method, device)

                    else:
                        LoggingManager.log_error(f"ClassroomManager.process_message(): Invalid Command Recieved {device}, {method_key}")

                LoggingManager.log_info("SweepWatcher.process_message(): Exiting")
                BlindManager.start()
                SweepWatcher._send_message()

            except serial.SerialException as e:
                RelayManager.close_connection()
                LoggingManager.log_error(f'ClassroomManager.process_message(): Error! {e}')

            except Exception as e:
                LoggingManager.log_error(f'ClassroomManager.process_message(): Error! {e}')
                catch_error_helper(e)

            #Batch all blind manager related commands so they stay in sync

        LoggingManager.log_info("SweepWatcher._check_sweep_dict(): Exiting")


    @staticmethod
    def _execute_command(method, qualifier):
        LoggingManager.log_info("SweepWatcher._execute_command(): Executing")
        if qualifier != "\"\"":
            method(qualifier)
        else:
            method()
        LoggingManager.log_info("SweepWatcher._execute_command(): Exiting")

    @staticmethod
    def _send_message():
        LoggingManager.log_info("SweepWatcher._send_message(): Executing")
        try:
            message = ConstantsManager.getInstance().current_values()
            SweepWatcher._connect()
            SweepWatcher._channel.basic_publish(exchange = Constants.CLIENT_EXCHANGE, routing_key = '', body = message)
            SweepWatcher._close()
        except Exception as e:
            LoggingManager.log_error(f"SweepWatcher.send_message: Connection error, {e}")
            raise HighLevelException("SweepWatcher", "_send_message", "RabbitMQ connection error", f"{e}")
        LoggingManager.log_info("SweepWatcher._send_message(): Exiting")

    @staticmethod
    def _connect():
        credentials = pika.PlainCredentials(Constants.USER_NAME, Constants.PASSWORD)
        parameters = pika.ConnectionParameters(Constants.IP_ADDRESS, Constants.PORT, Constants.VIRTUAL_BROKER, credentials, Constants.HEARTBEAT, blocked_connection_timeout = Constants.TIMEOUT)
        SweepWatcher._connection = pika.BlockingConnection(parameters)
        SweepWatcher._channel = SweepWatcher._connection.channel()


    @staticmethod
    def _close():
        LoggingManager.log_info("SweepWatcher._close(): Executing")
        SweepWatcher._channel.close()
        SweepWatcher._connection.close()
        SweepWatcher._channel = None
        SweepWatcher._connection = None
        LoggingManager.log_info("SweepWatcher._close(): Exiting")

