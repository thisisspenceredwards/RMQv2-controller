import subprocess
import HelperFunctions.Constants as Constants
from HelperFunctions.Exceptions import catch_error_helper
from HighLevelControls.Managers.LoggingManager import LoggingManager
from HighLevelControls.Managers.MessageManagers.Tables.RoomSettingsTable import RoomSettingsTable
from HighLevelControls.Managers.MessageManagers.Tables.SweepSettingsTable import SweepSettingsTable
from HighLevelControls.Managers.NotificationManager import NotificationManager
from HighLevelControls.Parser import ParsedMessage
from HighLevelControls.Managers.MessageManagers.Tables.DatabaseConnection import DatabaseConnection

class RoomSettingsManager:


    _set_hardware_clock = "sudo hwclock -w"

    _SETTINGS_MESSAGE = ParsedMessage(Constants.MQTT_TOPIC_NOTIFICATIONS, {Constants.SETTINGS_CURRENT_VALUES:""})

    _SWEEP_MESSAGE = ParsedMessage(Constants.MQTT_TOPIC_NOTIFICATIONS, {Constants.SWEEP_CURRENT_VALUES:""})

    _dict = {
        Constants.UPDATE_ROOM_ID: lambda val: RoomSettingsManager._update_room_id(val),
        Constants.UPDATE_WIND_THRESHOLD: lambda val: RoomSettingsManager._update_wind_threshold(val),
        Constants.CONTROLLER_TIME: lambda val: RoomSettingsManager._update_room_time(val),
        Constants.CREATE_SWEEP: lambda val: RoomSettingsManager._create_sweep(val),
        Constants.DELETE_SWEEP: lambda val: RoomSettingsManager._delete_sweep(val)
    }

    _response_dict = {
        Constants.UPDATE_ROOM_ID: lambda: RoomSettingsManager._SETTINGS_MESSAGE,
        Constants.UPDATE_WIND_THRESHOLD: lambda: RoomSettingsManager._SETTINGS_MESSAGE,
        Constants.CONTROLLER_TIME: lambda: RoomSettingsManager._SETTINGS_MESSAGE,
        Constants.CREATE_SWEEP: lambda: RoomSettingsManager._SWEEP_MESSAGE,
        Constants.DELETE_SWEEP: lambda: RoomSettingsManager._SWEEP_MESSAGE
    }

    @staticmethod
    @DatabaseConnection.DatabaseConnection
    def process_message(parsed_message):
        LoggingManager.log_info("RoomSettingsManager.process_message(): Executing")

        try:
            RoomSettingsTable.create_table_if_not_exist()
            SweepSettingsTable.create_table_if_not_exist()
            devices = {}
            for device, method_key in parsed_message.dictionary.items():
                function = RoomSettingsManager._dict[device]
                devices[device] = device
                if function is None:
                    continue
                function(method_key)


            for device in devices.values():
                parsed_messages = RoomSettingsManager._response_dict[device]()
                NotificationManager.process_message(parsed_messages)



        except Exception as e:
            LoggingManager.log_info(f"RoomSettingsManager.process_message(): error: {e}")
            catch_error_helper(e)

        LoggingManager.log_info("RoomSettingsManager.process_message(): Exiting")


    @staticmethod
    def _update_wind_threshold(val):
        LoggingManager.log_info("RoomSettingsManager._update_wind_threshold(): Executing")
        val = float(val)
        RoomSettingsTable.update_wind_threshold(val)
        Constants.MAXIMUM_ALLOWABLE_WIND_SPEED = val
        LoggingManager.log_info("RoomSettingsManager._update_wind_threshold(): Exiting")

    @staticmethod
    def _update_room_id(val):
        LoggingManager.log_info("RoomSettingsManager._update_room_id(): Executing")
        val = str(val)
        RoomSettingsTable.update_room_id(val)
        Constants.room_id.value = val
        LoggingManager.log_info("RoomSettingsManager._update_room_id(): Exiting")

    @staticmethod
    def _update_room_time(val):
        LoggingManager.log_error(f"RoomSettingsManager._update_room_time: Executing")
        try:
            time = str(val)
            set_date_command = f"sudo date --set=\"@{time}\""
            subprocess.run([set_date_command], shell = True)
            subprocess.run(RoomSettingsManager._set_hardware_clock, shell = True)
            subprocess.run("sudo timedatectl set-timezone UTC", shell = True) #Might not be needed...
            parsed_messages = ParsedMessage(Constants.MQTT_TOPIC_NOTIFICATIONS, {"SETTINGS_CURRENT_VALUES":""})
            NotificationManager.process_message(parsed_messages)

        except Exception as e:
            LoggingManager.log_error(f"RoomSettingsManager.process_message: Error! {e}")

        LoggingManager.log_error(f"RoomSettingsManager._update_room_time: Exiting")


    @staticmethod
    def _create_sweep(val):
        LoggingManager.log_error(f"RoomSettingsManager._create_sweep: Executing")
        SweepSettingsTable.insert(val)
        LoggingManager.log_error(f"RoomSettingsManager._create_sweep: Exiting")


    @staticmethod
    def _delete_sweep(val):
        LoggingManager.log_error(f"RoomSettingsManager._delete_sweep: Executing")
        SweepSettingsTable.delete(val)
        LoggingManager.log_error(f"RoomSettingsManager._delete_sweep: Exiting")
