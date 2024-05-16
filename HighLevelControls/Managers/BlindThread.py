import time
import threading
from HighLevelControls.Controller import Controller
from HighLevelControls.Managers.LoggingManager import LoggingManager
from HighLevelControls.Managers.RelayManager import RelayManager
from timeit import default_timer as timer
import HelperFunctions.BlindObjects as BlindObjects
import HelperFunctions.Constants as Constants

class BlindThread(threading.Thread):


    def __init__(self, sleep_duration = Constants.BLIND_THREAD_SLEEP_TIME):
        LoggingManager.log_info("BlindThread.init(): Called")
        threading.Thread.__init__(self)
        self._sleep_duration = sleep_duration
        self._stop_event = threading.Event()
        LoggingManager.log_info("BlindThread.init(): Complete")

    def run(self):
        LoggingManager.log_info("BlindThread.run(): Starting")
        RelayManager.getInstance().manually_refresh()
        while not self._stop_event.isSet():
            LoggingManager.log_info("BlindThread.run(): Executing")
            time_start = timer()
            list_to_remove = []
            active_dict = BlindObjects.ACTIVE_DICT.items()
            relays_to_turn_off = []
            for key, value in active_dict:
                #We end up turning off by a grouping of two, so we need the first smaller indexed relay
                starting_relay = value.run(self._sleep_duration)
                if starting_relay is not None:
                    list_to_remove.append(key)
                    relays_to_turn_off.append(starting_relay)

            if len(active_dict) == 0:
                self.stop()

            for item in list_to_remove:
                BlindObjects.ACTIVE_DICT.pop(item)

            if len(relays_to_turn_off) > 0:
                Controller.turn_off_all_blind_relays(relays_to_turn_off)
                RelayManager.getInstance().manually_refresh()

            time_end = timer()
            total_time = time_end - time_start
            sleep = self._sleep_duration - total_time
            #print(sleep)
            if sleep > 0:
                time.sleep(sleep)

            time.sleep(self._sleep_duration)
        LoggingManager.log_warn("BlindThread.run(): Thread has been stopped")

    def stop(self):
        LoggingManager.log_warn("BlindThread.stop(): Executing")
        self._stop_event.set()
        LoggingManager.log_warn("BlindThread.stop(): Exiting")
