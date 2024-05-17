import json
import HelperFunctions.Constants as Constants
from HighLevelControls.Managers.LoggingManager import LoggingManager
import HelperFunctions.BlindObjects as BO
import time
class ConstantsManager:


    _instance = None


    @staticmethod
    def getInstance():
        if ConstantsManager._instance is None:
            ConstantsManager._instance = ConstantsManager()
        return ConstantsManager._instance

    @staticmethod
    def _compile_values(dict_to_compile):
        temp_dict = {}
        for key, obj in dict_to_compile.items():
            temp_dict[key] = obj.value
        return temp_dict

    @staticmethod
    def current_values():
        LoggingManager.log_info("ConstantsManager.currentValues(): Executing")
        temp_dict = ConstantsManager._compile_values(Constants.CLASSROOM_DICT)
        temp_dict[Constants.MAC_ADDRESS_KEY] = Constants.MAC_ADDRESS
        LoggingManager.log_info("ConstantsManager.currentValues(): Exiting")
        return json.dumps(temp_dict)

    @staticmethod
    def current_wind_sensor_values():
        LoggingManager.log_info("ConstantsManager.current_wind_sensor_values(): Executing")

        temp_dict = ConstantsManager._compile_values(Constants.WIND_DICTIONARY)
        LoggingManager.log_info("ConstantsManager.current_wind_sensor_values(): Exiting")
        return json.dumps(temp_dict)

    @staticmethod
    def settings_current_values():
        LoggingManager.log_info("ConstantsManager.settings_current_values(): Executing")
        settings_dict = {}
        for key, obj in BO.BLIND_DICT.items():
            settings_dict[f"{key}_{Constants.TIME_TO_MIDDLE}"] = round(obj.blind_location_middle,2)
            settings_dict[f"{key}_{Constants.TIME_TO_BOTTOM}"] = round(obj.blind_location_bottom, 2)

        settings_dict[Constants.WIND_SPEED_AUTO_RAISE_THRESHOLD_KEY] = Constants.WIND_SPEED_MAXIMUM_FOR_AUTO_RAISE_THRESHOLD
        settings_dict[Constants.WIND_SPEED_LOWER_LOCK_THRESHOLD_KEY] = Constants.WIND_SPEED_MAXIMUM_FOR_LOWER_LOCK_THRESHOLD
        settings_dict[Constants.ROOM_ID_KEY] = Constants.room_id.value
        settings_dict[Constants.CONTROLLER_TIME] = time.clock_gettime(time.CLOCK_REALTIME)
        LoggingManager.log_info("ConstantsManager.settings_current_values(): Exiting")
        return json.dumps(settings_dict)

    @staticmethod
    def sweep_current_values():
        LoggingManager.log_info("ConstantsManager.sweep_current_values(): Executing")
        sweep_dict = {}

        sweep_list = ""
        for sweep in Constants.SWEEP_DICT.values():
            sweep_list += sweep + ","

        sweep_dict["CONTROLLER_SWEEP"] = sweep_list
        LoggingManager.log_info("ConstantsManager.sweep_current_values(): Exiting")
        return json.dumps(sweep_dict)
