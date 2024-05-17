import re
import serial
import HelperFunctions.Constants as Constants
from HighLevelControls.Managers.LoggingManager import LoggingManager
from HelperFunctions.Exceptions import LocalException

class WindSensorManager:


    _serial_connection = None
    _instance = None
    _RETRIEVE_UNIT_IDENTIFIER = "?&"
    _REGEX_PATTERN_FOR_IDENTIFIER = re.compile("[^a-zA-Z]")
    _duration_of_high_wind = 0


    @staticmethod
    def getInstance():
        LoggingManager.log_info("WindSensorManager.getInstance: Executing")
        if WindSensorManager._instance is None:
            WindSensorManager._instance = WindSensorManager()
            try:
                WindSensorManager._serial_connection = serial.Serial('/dev/serial0', 9600, timeout = 2, write_timeout = 2)
            except Exception as e:
                LoggingManager.log_error(f"WindSensorManager.getInstance: Failed {e}")

        LoggingManager.log_info("WindSensorManager.getInstance: Exiting")
        return WindSensorManager._instance


    @staticmethod
    def _get_unit_identifier():
        LoggingManager.log_info("WindSensorManager.get_unit_identifier: Executing")
        WindSensorManager._serial_connection.write(str.encode(WindSensorManager._RETRIEVE_UNIT_IDENTIFIER))
        response = WindSensorManager._serial_connection.readline().decode('utf-8')
        identifier = WindSensorManager._REGEX_PATTERN_FOR_IDENTIFIER.sub("", response)
        if response == "" or len(identifier) != 1:
            Constants.WIND_DICTIONARY[Constants.WIND_SENSOR_STATUS_KEY].value = Constants.WIND_SENSOR_UNABLE_TO_READ_WIND_SENSOR
            raise LocalException("WindSensorManager", "_get_unit_identifier", "No output from sensor")

        LoggingManager.log_info("WindSensorManager.get_unit_identifier: Exiting")
        return identifier


    @staticmethod
    def _remove_footer(sensor_input):
        index = sensor_input.rfind(',')
        slice_object = slice(0, index)
        return sensor_input[slice_object]


    @staticmethod
    def _remove_header(sensor_input):
        slice_object = slice(3, len(sensor_input))
        return sensor_input[slice_object]


    @staticmethod
    def _get_data(sensor_id):
        WindSensorManager._serial_connection.write(str.encode(sensor_id))
        return WindSensorManager._serial_connection.readline().decode("utf-8")


    @staticmethod
    def _parse_data(data):
        LoggingManager.log_info("WindSensorManager.parse_data: Executing")
        data_footer_removed = WindSensorManager._remove_footer(data)
        data_header_footer_removed = WindSensorManager._remove_header(data_footer_removed)
        data_as_list = data_header_footer_removed.split(',')
        data_dict = {
                     Constants.WIND_SENSOR_DIRECTION_KEY: data_as_list[0],
                      Constants.WIND_SENSOR_SPEED_KEY: data_as_list[1],
                       Constants.WIND_SENSOR_UNITS_KEY: data_as_list[2],
                        Constants.WIND_SENSOR_STATUS_KEY: data_as_list[3],
                    }
        LoggingManager.log_info("WindSensorManager.parse_data: Exiting")
        return data_dict


    @staticmethod
    def _update_global_dict(wind_dict):
        Constants.WIND_DICTIONARY[Constants.WIND_SENSOR_DIRECTION_KEY].value = wind_dict[Constants.WIND_SENSOR_DIRECTION_KEY]
        Constants.WIND_DICTIONARY[Constants.WIND_SENSOR_SPEED_KEY].value = wind_dict[Constants.WIND_SENSOR_SPEED_KEY]
        Constants.WIND_DICTIONARY[Constants.WIND_SENSOR_UNITS_KEY].value = wind_dict[Constants.WIND_SENSOR_UNITS_KEY]
        Constants.WIND_DICTIONARY[Constants.WIND_SENSOR_STATUS_KEY].value = wind_dict[Constants.WIND_SENSOR_STATUS_KEY]
        Constants.WIND_DICTIONARY[Constants.WIND_SPEED_BELOW_AUTO_RAISE_THRESHOLD_KEY].value = wind_dict[Constants.WIND_SPEED_BELOW_AUTO_RAISE_THRESHOLD_KEY]


    @staticmethod
    def _check_windspeed(wind_dict):
        LoggingManager.log_info("WindSensorManager.check_windspeeed: Executing")
        wind_speed = wind_dict[Constants.WIND_SENSOR_SPEED_KEY]
        float_wind_speed = float(wind_speed)
        LoggingManager.log_info(f"WindSensorManager._check_windspeed: {Constants.WIND_SPEED_MAXIMUM_FOR_AUTO_RAISE_THRESHOLD}")
        if float_wind_speed > Constants.WIND_SPEED_MAXIMUM_FOR_AUTO_RAISE_THRESHOLD:
            WindSensorManager._duration_of_high_wind = 1 if WindSensorManager._duration_of_high_wind == 0 else 2
            LoggingManager.log_warn(f"WindSensorManager.check_windspeed: duration of high wind {WindSensorManager._duration_of_high_wind}")

        else:
            WindSensorManager._duration_of_high_wind = 0


        if WindSensorManager._duration_of_high_wind >= 2:
            wind_dict[Constants.WIND_SPEED_BELOW_AUTO_RAISE_THRESHOLD_KEY] = False


        #RAISE THE SHADES
        else:
            wind_dict[Constants.WIND_SPEED_BELOW_AUTO_RAISE_THRESHOLD_KEY] = True


        LoggingManager.log_info("WindSensorManager.check_windspeeed: Exiting")
        return wind_dict


    @staticmethod
    def poll_sensor():
        LoggingManager.log_info("WindSensorManager.poll_sensor: Executing")

        try:
            wind_id = WindSensorManager._get_unit_identifier()
            unparsed_data = WindSensorManager._get_data(wind_id)
            data_dict = WindSensorManager._parse_data(unparsed_data)
            finalized_dict = WindSensorManager._check_windspeed(data_dict)
            LoggingManager.log_info(f"WindSensorManager.poll_sensor: {finalized_dict}")
            WindSensorManager._update_global_dict(finalized_dict)

        except Exception as e:
            LoggingManager.log_error(f"WindSensorManager.poll_sensor: Error {e}")
            Constants.WIND_DICTIONARY[Constants.WIND_SENSOR_STATUS_KEY].value = Constants.WIND_SENSOR_UNABLE_TO_READ_WIND_SENSOR

        LoggingManager.log_info("WindSensorManager.poll_sensor: Exiting")




