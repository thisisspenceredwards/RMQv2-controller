import HelperFunctions.Constants as Constants
from HighLevelControls.Controller import Controller
from HighLevelControls.Managers.LoggingManager import LoggingManager
from HighLevelControls.Managers.RelayManager import RelayManager
import HelperFunctions.BlindObjects as BlindObjects
from HighLevelControls.Managers.BlindThread import BlindThread
from HighLevelControls.Managers.IndividualBlind import IndividualBlind
class BlindManager:


    _blind_thread = None
    _arr = [[Constants.BLIND_ONE_KEY, Constants.BLIND_POSITION_TOP],
            [Constants.BLIND_TWO_KEY, Constants.BLIND_POSITION_TOP],
             [Constants.BLIND_THREE_KEY, Constants.BLIND_POSITION_TOP],
              [Constants.BLIND_FOUR_KEY, Constants.BLIND_POSITION_TOP],
               [Constants.BLIND_FIVE_KEY, Constants.BLIND_POSITION_TOP],
                [Constants.BLIND_SIX_KEY, Constants.BLIND_POSITION_TOP],
                 [Constants.BLIND_SEVEN_KEY, Constants.BLIND_POSITION_TOP],
                  [Constants.BLIND_EIGHT_KEY, Constants.BLIND_POSITION_TOP]]

    _pre_staging_dict = {}

    @staticmethod
    def _open_relay(blind_object):
        LoggingManager.log_info("BlindManager._open_relay: Executing")
        direction = blind_object.get_current_direction()
        relay_arr = blind_object.get_relays()
        if direction == IndividualBlind.BLIND_DIRECTION_UP:
            Controller.move_blind_up(relay_arr)

        elif direction == IndividualBlind.BLIND_DIRECTION_DOWN:
            Controller.move_blind_down(relay_arr)

        else:
            pass

        LoggingManager.log_info("BlindManager._open_relay: Exiting")

    #this and thread are the only place in the app .manually_refresh should be called
    #manually refresh is here because it makes the delay between starting the timer and refreshing as small as possible
    @staticmethod
    def handle_thread():
        LoggingManager.log_info("BlindManager._handle_thread: Executing")

        if BlindManager._blind_thread is None or not BlindManager._blind_thread.is_alive() and BlindObjects.ACTIVE_DICT:
            BlindManager._blind_thread = BlindThread()
            BlindManager._blind_thread.start()

        else:
            RelayManager.getInstance().manually_refresh()

        LoggingManager.log_info("BlindManager._handle_thread: Thread was dead -- created thread, Exiting")


    @staticmethod
    def _insert_into_prestage_dict(name, blind_object):
        LoggingManager.log_info("BlindManager._insert_into_prestage_dict: Executing")
        if name not in BlindManager._pre_staging_dict:
            BlindManager._pre_staging_dict[name] = blind_object
        LoggingManager.log_info("BlindManager._insert_into_prestage_dict: Exiting")


    @staticmethod
    def _set_new_blind_value(individual_blind_object, new_location):
        LoggingManager.log_info("BlindManager._set_new_blind_value: Executing")
        individual_blind_object.set_blind_value_object(new_location)
        LoggingManager.log_info("BlindManager._set_new_blind_value: Exiting")

    @staticmethod
    def _check_current_blind_value_is_at_location(individual_blind_object, new_location):
        if individual_blind_object.get_blind_value() == new_location:
            return True
        return False

    #this should only ever be called from ClassroomManager
    @staticmethod
    def on_message(name, location):
        LoggingManager.log_info("BlindManager.on_message: Executing")
        #gets the individualShade object
        blind_object = BlindObjects.BLIND_DICT[name]

        if not Constants.WIND_DICTIONARY[Constants.WIND_SENSOR_SPEED_BELOW_THRESHOLD_KEY].value and location != Constants.BLIND_POSITION_TOP:
            LoggingManager.log_info("BlindManager.on_message: Wind speed is above threshold and blinds are not at top position. Exiting")
            return

        if BlindManager._check_current_blind_value_is_at_location(blind_object, location):
            LoggingManager.log_info("BlindManager.on_message: Already at location. Exiting")
            return

        #this propogates changes down to everything else
        BlindManager._set_new_blind_value(blind_object, location)
        blind_object.update_to_new_direction()
        BlindManager._insert_into_prestage_dict(name, blind_object)
        LoggingManager.log_info("BlindManager.on_message: Exiting")


    @staticmethod
    def start():
        LoggingManager.log_info("BlindManager.start: Executing")
        BlindObjects.ACTIVE_DICT = BlindObjects.ACTIVE_DICT | BlindManager._pre_staging_dict # merge dictionaries
        for key, value in BlindManager._pre_staging_dict.items():
            BlindManager._open_relay(value)

        BlindManager.handle_thread()
        BlindManager._pre_staging_dict = {}
        LoggingManager.log_info("BlindManager.start: Exiting")


    @staticmethod
    def set_blinds_to_top_position_high_wind():
        LoggingManager.log_info("BlindManager.set_blind_to_top_position_high_wind: Executing")
        for entry in BlindManager._arr:
            obj = BlindObjects.BLIND_DICT[entry[0]]
            if obj.get_current_position() >  Constants.BLIND_POSITION_TOP:
                BlindManager.on_message(entry[0], entry[1])

        BlindManager.start()
        LoggingManager.log_info("BlindManager.set_blind_to_top_position_high_wind: Exiting")


    @staticmethod
    def set_blinds_to_top_position():
        LoggingManager.log_info("BlindManager.set_blind_to_top_position: Executing")
        #Make sure connection is valid
        for entry in BlindManager._arr:
            BlindManager.on_message(entry[0], entry[1])

        BlindManager.start()
        LoggingManager.log_info("BlindManager.set_blind_to_top_position: Exiting")

