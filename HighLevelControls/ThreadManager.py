import time
import threading
import HelperFunctions.Constants as Constants
from HighLevelControls.Managers.LoggingManager import LoggingManager

class ThreadManager(threading.Thread):


    def __init__(self, method):
        LoggingManager.log_info("ThreadManager.init(): Called")
        threading.Thread.__init__(self)
        self._method = method
        self._stop_event = threading.Event()
        LoggingManager.log_info("ThreadManager.init(): Complete")

    def run(self):
        LoggingManager.log_info("ThreadManager.run(): Starting")
        while not self._stop_event.isSet():
            LoggingManager.log_info("ThreadManager.run(): Executing")
            self._method()
            time.sleep(Constants.GENERIC_THREAD_SLEEP_TIME)
        LoggingManager.log_warn("ThreadManager.run(): Thread has been stopped")

    def stop(self):
        LoggingManager.log_info("ThreadManager.stop(): Executing")
        self._stop_event.set()
        LoggingManager.log_info("ThreadManager.stop(): Exiting")
