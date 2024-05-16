import serial
from serial.tools import list_ports
import HelperFunctions.Constants as Constants
from HelperFunctions.Exceptions import LocalException
from HighLevelControls.Managers.ncd_industrial_relay import Relay_Controller
from HighLevelControls.Managers.LoggingManager import LoggingManager
from threading import Lock
import time
class RelayManager:

    _lock = Lock()

    COMMAND_SET_TO_MANUAL = [254, 26]
    BYTES_BACK = 4
    _relay_com_obj = None
    _serial_connection = None
    _instance = None
    _STATUS = Constants.CLASSROOM_DICT.get(Constants.RELAY_BOARD_STATUS_KEY)
    
    @staticmethod
    def _get_port():
        for port in list(serial.tools.list_ports.comports()):
            split = str(port).split("-")
            if len(split) >= 2:
                port_addr  = split[0]
                device_name = split[1]
                if Constants.NAME_OF_RELAY_BOARD in device_name:
                    return port_addr.strip() #remove any whitespace

    @staticmethod
    def close_connection():
        RelayManager._relay_com_obj = None
        RelayManager._serial_connection = None

    @staticmethod
    def getInstance():
        LoggingManager.log_info("RelayManager.getInstance(): Executing")
        if RelayManager._instance is None:
            RelayManager._instance = RelayManager()

        port_addr = RelayManager._get_port()
        if port_addr is None:
            RelayManager._STATUS.value = Constants.ERROR_VALUE
            raise LocalException("RelayManager", "getInstance", "Relayboard is not connected")

        if RelayManager._serial_connection is not None:
            LoggingManager.log_info("RelayManager.getInstance(): returning existing instance")
            return RelayManager._instance

        try:
            #find port that board is in and return it
            LoggingManager.log_info("RelayManager.getInstance(): Creating Connection")
            RelayManager._serial_connection = serial.Serial(port_addr, baudrate = 115200, timeout = 1)
            RelayManager._relay_com_obj = Relay_Controller(RelayManager._serial_connection)
            command = RelayManager._relay_com_obj.wrap_in_api(RelayManager.COMMAND_SET_TO_MANUAL)
            RelayManager._relay_com_obj.send_command(command, RelayManager.BYTES_BACK)
            RelayManager._STATUS.value = Constants.OK_VALUE
            LoggingManager.log_info("RelayManager.getInstance(): Exiting")
            return RelayManager._instance

        except Exception as e:
            RelayManager._set_error()
            LoggingManager.log_error(f"RelayManager.getInstance(): Opening serial connection failed {e}")



    @staticmethod
    def turn_off_relay(relay):
        LoggingManager.log_info("RelayManager.turn_off_relay: Executing")
        try:
            RelayManager._lock.acquire()
            RelayManager.getInstance()
            response = RelayManager._relay_com_obj.turn_off_relay_by_index(relay)
            RelayManager._check_response(response)
            RelayManager._lock.release()

        except Exception as e:
            RelayManager._lock.release()
            RelayManager._set_error()

        LoggingManager.log_info("RelayManager.turn_off_relay: Exiting")

    @staticmethod
    def turn_off_blind_relays_by_group(starting_relay):
        #will only turn off two relays, only used for blinds
        LoggingManager.log_info("RelayManager.turn_off_blind_relays_by_group: Executing")
        try:
            RelayManager._lock.acquire()
            RelayManager.getInstance()
            size_of_bank = 8
            group_size = 2
            bank = ((starting_relay - 1) / size_of_bank) + 1
            bank = int(bank)
            adjusted_relay_index = starting_relay % size_of_bank
            if adjusted_relay_index == 0:
                adjusted_relay_index = 8
            RelayManager._relay_com_obj.turn_off_relay_group(adjusted_relay_index, bank, group_size)
            RelayManager._lock.release()
            LoggingManager.log_info("RelayManager.turn_off_blind_relays_by_group: Exiting")
        
        except Exception as e:
            RelayManager._lock.release()
            RelayManager._set_error()

    @staticmethod
    def turn_on_relay(relay):
        LoggingManager.log_info("RelayManager.turn_on_relay: Executing")
        try:
            RelayManager.getInstance()
            RelayManager._lock.acquire()
            response = RelayManager._relay_com_obj.turn_on_relay_by_index(relay)
            RelayManager._check_response(response)
            RelayManager._lock.release()
        
        except Exception as e:
            RelayManager._lock.release()
            RelayManager._set_error()

        LoggingManager.log_info("RelayManager.turn_on_relay: Exiting")

    @staticmethod
    def manually_refresh():
        LoggingManager.log_info("RelayManager.manually_refresh: Executing")

        try:
            RelayManager.getInstance()
            RelayManager._lock.acquire()
            command = RelayManager._relay_com_obj.wrap_in_api([254, 37])
            bytes_back = 4
            send_command = RelayManager._relay_com_obj.send_command
            response = RelayManager._relay_com_obj.process_control_command_return(send_command(command, bytes_back))
            RelayManager._check_response(response)
            RelayManager._lock.release()

        except Exception as e:
            RelayManager._lock.release()
            RelayManager._set_error()


    @staticmethod
    def _set_error():
        LoggingManager.log_error("RelayManager._set_error: Executing")
        RelayManager.close_connection()
        RelayManager._STATUS.value = Constants.ERROR_VALUE
        LoggingManager.log_error("RelayManager._set_error: Exiting")
        raise LocalException("RelayManager", "_check_response", "response from relay board indicates error")


    @staticmethod
    def _check_response(response):
        LoggingManager.log_info("RelayManager._check_response: Executing")
        # if handshake and bytes_back and checksum response contains True, else response contains False
        result = response[0]
        if result:
            RelayManager._STATUS.value = Constants.OK_VALUE

        else:
            RelayManager._set_error()

        LoggingManager.log_info("RelayManager._check_response: Exiting")
