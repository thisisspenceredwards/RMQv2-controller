import HelperFunctions.BlindObjects as BO
import HelperFunctions.Constants as Constants
from HelperFunctions.Exceptions import catch_error_helper
from HighLevelControls.Managers.LoggingManager import LoggingManager
from HighLevelControls.Managers.MessageManagers.Tables.BlindSettingsTable import BlindSettingsTable
from HighLevelControls.Managers.NotificationManager import NotificationManager
from HighLevelControls.Parser import ParsedMessage
from HighLevelControls.Managers.MessageManagers.Tables.DatabaseConnection import DatabaseConnection

class BlindSettingsManager:


    _blind_objects = BO.BLIND_DICT
    _dict = {
        "BLIND_ONE_TIME_TO_MIDDLE": lambda val: BlindSettingsManager._update_blind_middle(Constants.BLIND_ONE_KEY, val),
        "BLIND_ONE_TIME_TO_BOTTOM": lambda val: BlindSettingsManager._update_blind_bottom(Constants.BLIND_ONE_KEY, val),
        "BLIND_TWO_TIME_TO_MIDDLE": lambda val: BlindSettingsManager._update_blind_middle(Constants.BLIND_TWO_KEY, val),
        "BLIND_TWO_TIME_TO_BOTTOM": lambda val: BlindSettingsManager._update_blind_bottom(Constants.BLIND_TWO_KEY, val),
        "BLIND_THREE_TIME_TO_MIDDLE": lambda val: BlindSettingsManager._update_blind_middle(Constants.BLIND_THREE_KEY, val),
        "BLIND_THREE_TIME_TO_BOTTOM":lambda val: BlindSettingsManager._update_blind_bottom(Constants.BLIND_THREE_KEY, val),
        "BLIND_FOUR_TIME_TO_MIDDLE": lambda val: BlindSettingsManager._update_blind_middle(Constants.BLIND_FOUR_KEY, val),
        "BLIND_FOUR_TIME_TO_BOTTOM": lambda val: BlindSettingsManager._update_blind_bottom(Constants.BLIND_FOUR_KEY, val),
        "BLIND_FIVE_TIME_TO_MIDDLE": lambda val: BlindSettingsManager._update_blind_middle(Constants.BLIND_FIVE_KEY, val),
        "BLIND_FIVE_TIME_TO_BOTTOM": lambda val: BlindSettingsManager._update_blind_bottom(Constants.BLIND_FIVE_KEY, val),
        "BLIND_SIX_TIME_TO_MIDDLE": lambda val: BlindSettingsManager._update_blind_middle(Constants.BLIND_SIX_KEY, val),
        "BLIND_SIX_TIME_TO_BOTTOM": lambda val: BlindSettingsManager._update_blind_bottom(Constants.BLIND_SIX_KEY, val),
        "BLIND_SEVEN_TIME_TO_MIDDLE": lambda val: BlindSettingsManager._update_blind_middle(Constants.BLIND_SEVEN_KEY, val),
        "BLIND_SEVEN_TIME_TO_BOTTOM": lambda val: BlindSettingsManager._update_blind_bottom(Constants.BLIND_SEVEN_KEY, val),
        "BLIND_EIGHT_TIME_TO_MIDDLE": lambda val: BlindSettingsManager._update_blind_middle(Constants.BLIND_EIGHT_KEY,val),
        "BLIND_EIGHT_TIME_TO_BOTTOM": lambda val: BlindSettingsManager._update_blind_bottom(Constants.BLIND_EIGHT_KEY, val)
    }


    @staticmethod
    @DatabaseConnection.DatabaseConnection
    def process_message(parsed_message):
        LoggingManager.log_info("BlindSettingsManager.process_message(): Executing")
        try:
            BlindSettingsTable.create_table_if_not_exist()
            for device, method_key in parsed_message.dictionary.items():
                function = BlindSettingsManager._dict[device]
                if function is None:
                    continue
                function(method_key)

            parsed_messages = ParsedMessage(Constants.MQTT_TOPIC_NOTIFICATIONS, {"SETTINGS_CURRENT_VALUES":""})
            NotificationManager.process_message(parsed_messages)
        #Should not interupt app execution so catch all
        except Exception as e:
            LoggingManager.log_info(f"BlindSettingsManager.process_message(): error: {e}")
            catch_error_helper(e)
        LoggingManager.log_info("BlindSettingsManager.process_message(): Exiting")


    @staticmethod
    def _update_blind_middle(blind, val):
        LoggingManager.log_info("BlindSettingsManager._update_blind_middle(): Executing")
        val = float(val)
        BlindSettingsTable.update_entry(blind, time_to_middle = val, time_to_bottom = None)
        BlindSettingsManager._blind_objects[blind].update_blind_location_middle(val)
        LoggingManager.log_info("BlindSettingsManager._update_blind_middle(): Exiting")

    @staticmethod
    def _update_blind_bottom(blind, val):
        LoggingManager.log_info("BlindSettingsManager._update_blind_bottom(): Executing")
        val = float(val)
        BlindSettingsTable.update_entry(blind, time_to_middle = None, time_to_bottom = val)
        BlindSettingsManager._blind_objects[blind].update_blind_location_bottom(val)
        LoggingManager.log_info("BlindSettingsManager._update_blind_bottom(): Exiting")
