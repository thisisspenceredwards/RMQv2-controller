############
#File contains a class which controls the relays and turning off the machine
############
'''
    Notes: Receptacles_dict, Blinds_dict etc contain objects and below we are changing the value contained in these objects which are
    contained in the dictionaries, so the values are available through the entire program

'''
import os
import HelperFunctions.Constants as Constants
from HighLevelControls.Managers.LoggingManager import LoggingManager
from HighLevelControls.Managers.RelayManager import RelayManager

class Controller:


    @staticmethod
    def receptacle_on(recept):
        LoggingManager.log_info("Controller.receptacle_on: Executing")
        relay = Constants.RELAY_MAPPING_DICT.get(recept)
        recept_obj = Constants.RECEPTACLES_DICT.get(recept)
        if recept_obj.value != 1:
            RelayManager.turn_on_relay(relay)
            recept_obj.value = 1
        LoggingManager.log_info("Controller.receptacle_on: Exiting")


    @staticmethod
    def receptacle_off(recept):
        LoggingManager.log_info("Controller.receptacle_off: Executing")
        relay = Constants.RELAY_MAPPING_DICT.get(recept)
        recept_obj = Constants.RECEPTACLES_DICT.get(recept)
        if recept_obj.value != 0:
            RelayManager.turn_off_relay(relay)
            recept_obj.value = 0
        LoggingManager.log_info("Controller.receptacle_off: Exiting")


    @staticmethod
    def light_on(light):
        LoggingManager.log_info("Controller.light_on: Executing")
        relay = Constants.RELAY_MAPPING_DICT.get(light)
        light_obj = Constants.LIGHTS_DICT.get(light)
        if light_obj.value != 1:
            RelayManager.turn_on_relay(relay)
            light_obj.value = 1
        LoggingManager.log_info("Controller.light_on: Exiting")


    @staticmethod
    def light_off(light):
        LoggingManager.log_info("Controller.light_off: Executing")
        relay = Constants.RELAY_MAPPING_DICT.get(light)
        light_obj = Constants.LIGHTS_DICT.get(light)
        if light_obj.value != 0:
            RelayManager.turn_off_relay(relay)
            light_obj.value = 0
        LoggingManager.log_info("Controller.light_off: Exiting")

    @staticmethod
    def move_shade(shade, position):
        LoggingManager.log_info(f"Controller.move_shade {shade}: Executing")

        relay_arr = Constants.RELAY_MAPPING_DICT.get(shade)


        #do something
        # RelayManager.turn_on_relay(relay)
        # RelayManager.turn_off_relay(relay)


    @staticmethod
    def move_shades_to_top_position():
        LoggingManager.log_info('Controller.move_shades_to_top_position: Executing')
        #SEDWARDS: fix
        LoggingManager.log_info('Controller.move_shades_to_top_position: Exiting')


    @staticmethod
    def turn_off_all_blind_relays(relay_arr):
        LoggingManager.log_info("Controller.turn_off_all_blind_relays: Executing")
        for relay in relay_arr:
            RelayManager.turn_off_blind_relays_by_group(relay)

        LoggingManager.log_info("Controller.turn_off_all_blind_relays: Exiting")


    @staticmethod
    def shutdown(dummy_value = None):
        LoggingManager.log_warn("Controller.shutdown(): Executing")
        shutdown = Constants.CLASSROOM_DICT.get("SHUTDOWN")
        shutdown.value = 1
        os.system("sudo shutdown +1")


    @staticmethod
    def cancel_shutdown(dummy_value = None):
        LoggingManager.log_warn("Controller.cancel_shutdown(): Executing")
        shutdown = Constants.CLASSROOM_DICT.get("SHUTDOWN")
        shutdown.value = 0
        os.system("sudo shutdown -c")


    @staticmethod
    def turn_off_all_relays():
        #Must be updated for final system
        try:
            LoggingManager.log_info("Controller.turn_off_all_relays: Executing")
            for i in range(0, 41):
                RelayManager.turn_off_relay(i)

            for obj in Constants.BLINDS_DICT.values():
                obj.value = Constants.BLIND_POSITION_BOTTOM

            for obj in Constants.LIGHTS_DICT.values():
                obj.value = Constants.LIGHT_OFF

            for obj in Constants.RECEPTACLES_DICT.values():
                obj.value = Constants.RECEPTACLE_OFF

        except Exception as e:
            LoggingManager.log_info(f"Controller.turn_off_all_relays: Error: {e}")

        LoggingManager.log_info("Controller.turn_off_all_relays: Exiting")

