import HelperFunctions.Constants as Constants
from HighLevelControls.Managers.LoggingManager import LoggingManager

class IndividualBlind:


    #Time to go to confirm position
    BLIND_END_BUFFER = 2
    #Error range to determine when at a satisfactory middle position
    BLIND_MIDDLE_BUFFER = 0.15
    #Constants to determine direction
    BLIND_DIRECTION_DOWN = 1
    BLIND_DIRECTION_UP = -1
    BLIND_DIRECTION_STATIONARY = 0
    BLIND_POSITION_TOP = 0
    BLIND_POSITION_MIDDLE = 1
    BLIND_POSITION_BOTTOM = 2
    #BLIND_POSITION is a key ala 0, 1, 2 to indicate where it should be going
    #BLIND_DESITNATION is the timed distance the blind needs to go
    def __init__(self, blind_name, blind_object, blind_location_middle, blind_location_bottom):
        LoggingManager.log_info("IndividualBlind.__init__: Executing")
        self.blind_name = blind_name
        self.blind_location_top = 0 #is origin
        self.blind_location_middle = blind_location_middle
        self.blind_location_bottom = blind_location_bottom

        self._blind_object = blind_object
        self._current_destination = None
        self._current_position = self.blind_location_bottom
        self._current_direction = IndividualBlind.BLIND_DIRECTION_UP
        self._current_destination = self._convert_blind_value_to_destination()
        self._set_direction()
        LoggingManager.log_info("IndividualBlind.__init__: Exiting")


    def get_current_position(self):
        return self._current_position

    def get_current_direction(self):
        return self._current_direction

    def update_blind_location_middle(self, val):
        LoggingManager.log_info("IndividualBlind.update_blind_location_middle: Executing")
        self.blind_location_middle = val


    def update_blind_location_bottom(self, val):
        LoggingManager.log_info("IndividualBlind.update_blind_location_bottom: Executing")
        self.blind_location_bottom = val


    def _convert_blind_value_to_destination(self):
        LoggingManager.log_info("IndividualBlind._convert_blind_value_to_destination: Executing")
        value = self._blind_object.value
        if value == IndividualBlind.BLIND_POSITION_BOTTOM:
            LoggingManager.log_info("IndividualBlind._convert_blind_value_to_destination: LOCATION BOTTOM:  Exiting")
            return self.blind_location_bottom

        elif value == IndividualBlind.BLIND_POSITION_MIDDLE:
            LoggingManager.log_info("IndividualBlind._convert_blind_value_to_destination: LOCATION MIDDLE:  Exiting")
            return self.blind_location_middle

        else:
            LoggingManager.log_info("IndividualBlind._convert_blind_value_to_destination: LOCATION TOP:  Exiting")
            return self.blind_location_top


    def _set_direction(self):
        LoggingManager.log_info("IndividualBlind._set_direction: Executing")
        new_destination = self._convert_blind_value_to_destination()
        if new_destination == self.blind_location_top:
            self._current_direction = IndividualBlind.BLIND_DIRECTION_UP

        elif new_destination == self.blind_location_bottom:
            self._current_direction = IndividualBlind.BLIND_DIRECTION_DOWN

        else: #new destination is middle
            if self._current_position < self.blind_location_middle:
                self._current_direction = IndividualBlind.BLIND_DIRECTION_DOWN
            else:
                self._current_direction = IndividualBlind.BLIND_DIRECTION_UP


        LoggingManager.log_info("IndividualBlind._set_direction: Exiting")


    def compute_current_position(self, time_interval):
        LoggingManager.log_info("IndividualBlind._compute_current_position: Executing")
        self._current_position += self._current_direction * time_interval
        #print(self.blind_name, self._current_position)
        LoggingManager.log_info("IndividualBlind._compute_current_position: Exiting")


    def check_if_arrived(self):
        LoggingManager.log_info("IndividualBlind.check_if_arrived: Executing")
        if self._current_destination == self.blind_location_top:
            if self._current_position < (self.blind_location_top - IndividualBlind.BLIND_END_BUFFER):
                self._current_direction = IndividualBlind.BLIND_DIRECTION_STATIONARY
                self._current_position = self.blind_location_top
                LoggingManager.log_info("IndividualBlind.check_if_arrived: Arrived Top Exiting")
                return True

            LoggingManager.log_info("IndividualBlind.check_if_arrived: Not Arrived Top Exiting")
            return False

        elif self._current_destination == self.blind_location_middle:
            if abs(self._current_position - self.blind_location_middle) <= IndividualBlind.BLIND_MIDDLE_BUFFER:
                self._current_position = self.blind_location_middle
                self._current_direction = IndividualBlind.BLIND_DIRECTION_STATIONARY
                LoggingManager.log_info("IndividualBlind.check_if_arrived: Arrived Middle Exiting")
                return True

            LoggingManager.log_info("IndividualBlind.check_if_arrived: Not Arrived Middle Exiting")
            return False

        elif self._current_destination == self.blind_location_bottom:
           if self._current_position > (self.blind_location_bottom + IndividualBlind.BLIND_END_BUFFER):
               self._current_position = self.blind_location_bottom
               self._current_direction = IndividualBlind.BLIND_DIRECTION_STATIONARY
               LoggingManager.log_info("IndividualBlind.check_if_arrived: Arrived Bottom Exiting")
               return True

           LoggingManager.log_info("IndividualBlind.check_if_arrived: Not Arrived Bottom Exiting")
           return False

        else:
            raise Exception("IndividualBlind: compute_current_position error")


    def run(self, time_interval):
        #All run does is decide when to shut off the relays
        LoggingManager.log_info("IndividualBlind.run: Executing")
        self.compute_current_position(time_interval)
        if self.check_if_arrived():
            relays_to_turn_off = Constants.RELAY_MAPPING_DICT.get(self.blind_name)
            LoggingManager.log_info("IndividualBlind.run: Finished: Exiting")
            return min(relays_to_turn_off[0], relays_to_turn_off[1])

        LoggingManager.log_info("IndividualBlind.run: Not finished: Exiting")
        return None

    def get_relays(self):
        LoggingManager.log_info("IndividualBlind.get_relays: Executing")
        relay_arr = Constants.RELAY_MAPPING_DICT.get(self.blind_name)
        #always make sure device can get back to the top most position
        LoggingManager.log_info("IndividualBlind.get_relays: Exiting")
        return relay_arr


    def _set_current_position_if_still_running_buffer(self):
        LoggingManager.log_info("IndividualBlind._set_current_position_if_still_running_buffer: Executing")
        if self._current_position > self.blind_location_bottom:
            self._current_position = self.blind_location_bottom

        elif self._current_position < self.blind_location_top:
            self._current_position = self.blind_location_top
        LoggingManager.log_info("IndividualBlind._set_current_position_if_still_running_buffer: Exiting")


    def update_to_new_direction(self):
        LoggingManager.log_info("IndividualBlind.update_to_new_direction: Executing")
        self._set_direction()
        #this line must be below set_direction
        self._current_destination = self._convert_blind_value_to_destination()
        self._set_current_position_if_still_running_buffer()
        LoggingManager.log_info("IndividualBlind.update_to_new_direction: Executing")
        return self.get_relays()
        #else somewhere in the middle which doesn't need adjustment


    def set_blind_value_object(self, new_location):
        LoggingManager.log_info("IndividualBlind.set_blind_value_object: Executing")
        self._blind_object.value = new_location
        LoggingManager.log_info("IndividualBlind.set_blind_value_object: Exiting")


    def get_blind_value(self):
        LoggingManager.log_info("IndividualBlind.get_blind_value: Executing")
        LoggingManager.log_info("IndividualBlind.get_blind_value: Exiting")
        return self._blind_object.value


