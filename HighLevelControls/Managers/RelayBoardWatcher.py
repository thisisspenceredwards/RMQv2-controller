import pika
import serial
from serial.tools import list_ports
import time
import threading
import HelperFunctions.Constants as Constants
from HelperFunctions.Exceptions import HighLevelException
from HighLevelControls.Managers.RelayManager import RelayManager
from HighLevelControls.Managers.ConstantsManager import ConstantsManager
from HighLevelControls.Managers.LoggingManager import LoggingManager
from HighLevelControls.Managers.BlindManager import BlindManager


class RelayBoardWatcher(threading.Thread):


    _STATUS = Constants.CLASSROOM_DICT.get(Constants.RELAY_BOARD_STATUS_KEY)
    _connection = None
    _channel = None
    _wind_sensor_error_flag = False
    _shades_disabled = False

    @staticmethod
    def _connect():
        credentials = pika.PlainCredentials(Constants.USER_NAME, Constants.PASSWORD)
        parameters = pika.ConnectionParameters(Constants.IP_ADDRESS, Constants.PORT, Constants.VIRTUAL_BROKER, credentials, Constants.HEARTBEAT, blocked_connection_timeout = Constants.TIMEOUT)
        RelayBoardWatcher._connection = pika.BlockingConnection(parameters)
        RelayBoardWatcher._channel = RelayBoardWatcher._connection.channel()

    @staticmethod
    def _close():
        LoggingManager.log_info("RelayBoardWatcher._close(): Executing")
        RelayBoardWatcher._channel.close()
        RelayBoardWatcher._connection.close()
        LoggingManager.log_info("RelayBoardWatcher._close(): Exiting")


    def __init__(self, sleep_duration = 5):
        LoggingManager.log_info("RelayBoardWatcher.init(): Called")
        threading.Thread.__init__(self)
        self.sleep_duration = sleep_duration
        self._stop_event = threading.Event()
        LoggingManager.log_info("RelayBoardWatcher.init(): Complete")


    def run(self):
        LoggingManager.log_info("RelayBoardWatcher.run(): Starting")
        while not self._stop_event.isSet():
            LoggingManager.log_info("RelayBoardWatcher.run(): Executing")
            RelayBoardWatcher.watch_connection()
            RelayBoardWatcher.check_wind_speed_flag()
            RelayBoardWatcher.check_wind_sensor_status_flag()
            time.sleep(self.sleep_duration)
        LoggingManager.log_warn("RelayBoardWatcher.run(): Thread has been stopped")


    def stop(self):
        LoggingManager.log_info("RelayBoardWatcher.stop(): Executing")
        self._stop_event.set()
        LoggingManager.log_info("RelayBoardWatcher.stop(): Exiting")


    @staticmethod
    def check_wind_sensor_status_flag():
        LoggingManager.log_info("RelayBoardWatcher.check_wind_sensor_status_flag: Executing")

        status = Constants.WIND_DICTIONARY[Constants.WIND_SENSOR_STATUS_KEY].value
        if status != Constants.OK_VALUE and not RelayBoardWatcher._wind_sensor_error_flag:
            LoggingManager.log_info(f"RelayBoardWatcher.check_wind_sensor_status_flag: Wind sensor reports error {status}")
            RelayBoardWatcher._wind_sensor_error_flag = True
            RelayBoardWatcher._send_message()
        elif status == Constants.OK_VALUE and RelayBoardWatcher._wind_sensor_error_flag:
            LoggingManager.log_info("RelayBoardWatcher.check_wind_speed_flag: Normal operations regained")
            RelayBoardWatcher._wind_sensor_error_flag = False
            RelayBoardWatcher._send_message()

        LoggingManager.log_info("RelayBoardWatcher.check_wind_sensor_flag: Exiting")


    @staticmethod
    def check_wind_speed_flag():
        LoggingManager.log_info("RelayBoardWatcher.check_wind_speed_flag: Executing")

        if not Constants.WIND_DICTIONARY[Constants.WIND_SPEED_BELOW_AUTO_RAISE_THRESHOLD_KEY].value and not RelayBoardWatcher._shades_disabled:
            LoggingManager.log_info("RelayBoardWatcher.check_wind_speed_flag: Wind speed is above threshold")
            BlindManager.set_blinds_to_top_position_high_wind()
            RelayBoardWatcher._shades_disabled = True
            RelayBoardWatcher._send_message()
        #Wind is now below threshold we need to update iPad
        elif Constants.WIND_DICTIONARY[Constants.WIND_SPEED_BELOW_AUTO_RAISE_THRESHOLD_KEY].value and RelayBoardWatcher._shades_disabled:
            LoggingManager.log_info("RelayBoardWatcher.check_wind_speed_flag: Wind speed is below threshold")
            RelayBoardWatcher._shades_disabled = False
            RelayBoardWatcher._send_message()

        LoggingManager.log_info("RelayBoardWatcher.check_wind_speed_flag: Exiting")


    @staticmethod
    def _send_message():
        LoggingManager.log_info("RelayBoardWatcher._send_message(): Executing")
        try:
            message = ConstantsManager.getInstance().current_values()
            RelayBoardWatcher._connect()
            RelayBoardWatcher._channel.basic_publish(exchange = Constants.CLIENT_EXCHANGE, routing_key = '', body = message)
            RelayBoardWatcher._close()
        except Exception as e:
            LoggingManager.log_error(f"RelayBoardWatcher.send_message: Connection error, {e}")
            raise HighLevelException("RelayBoardWatcher", "_send_message", "RabbitMQ connection error", f"{e}")
        LoggingManager.log_info("RelayBoardWatcher._send_message(): Exiting")


    @staticmethod
    def watch_connection():
        LoggingManager.log_info("RelayBoardWatcher._watch_connection(): Executing")
        port_exists = False
        for port in list(serial.tools.list_ports.comports()):
            port = str(port)
            if Constants.NAME_OF_RELAY_BOARD in port:
                port_exists = True

        if not port_exists and RelayBoardWatcher._STATUS.value == Constants.OK_VALUE:
            try:
                RelayBoardWatcher._STATUS.value = Constants.ERROR_NOT_FOUND_VALUE
                RelayBoardWatcher._send_message()
                LoggingManager.log_info("RelayBoardWatcher.watch_connection(): Disconnection -- Message success")

            #catch all exceptions as relay board should not interrupt app execution
            except Exception as e:
                RelayBoardWatcher._STATUS.value = Constants.OK_VALUE #reset state
                LoggingManager.log_info("RelayBoardWatcher.watch_connection(): Disconnection -- Sending message failed {e}")

        elif port_exists and RelayBoardWatcher._STATUS.value == Constants.ERROR_NOT_FOUND_VALUE:
            try:
                RelayBoardWatcher._STATUS.value = Constants.OK_VALUE
                #attempt to remake connection
                RelayManager.close_connection()
                RelayManager.getInstance()
                RelayBoardWatcher._send_message()
                LoggingManager.log_info("RelayBoardWatcher.watch_connection(): Reconnection -- Sending message success")

            #catch all exceptions as relay board should not interrupt app execution
            except Exception as e:
                RelayBoardWatcher._STATUS.value = Constants.ERROR_NOT_FOUND_VALUE
                LoggingManager.log_info(f"RelayBoardWatcher.watch_connection(): Reconnection -- Sending message failed {e}")

        LoggingManager.log_info("RelayBoardWatcher._watch_connection(): Exiting")
