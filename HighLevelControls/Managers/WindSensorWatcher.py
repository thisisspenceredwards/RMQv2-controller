import time
import threading
from HighLevelControls.Managers.WindSensorManager import WindSensorManager
from HighLevelControls.Managers.ConstantsManager import ConstantsManager
from HighLevelControls.Managers.LoggingManager import LoggingManager


class WindSensorWatcher(threading.Thread):


    _wind_sensor_manager = WindSensorManager.getInstance()
    _constants_manager = ConstantsManager.getInstance()


    def __init__(self, sleep_duration = 5):
        LoggingManager.log_info("WindSensorWatcher.init(): Called")
        threading.Thread.__init__(self)
        self.sleep_duration = sleep_duration
        self._stop_event = threading.Event()
        LoggingManager.log_info("WindSensorWatcher.init(): Complete")


    def run(self):
        LoggingManager.log_info("WindSensorWatcher.run(): Starting")
        while not self._stop_event.isSet():
            LoggingManager.log_info("WindSensorWatcher.run(): Executing")
            try:
                #In the instance of high wind the dictionary value is set to the corresponding value,
                #In RelayBoardWatcher the relays are turned off accordingly and a message to the client is sent
                WindSensorWatcher._wind_sensor_manager.poll_sensor()

            #Catch all exceptions as the wind sensor should not interrupt the apps execution
            except Exception as e:
                LoggingManager.log_error(f"WindSensorWatcher.run(): Error polling wind sensor {e}")
            time.sleep(self.sleep_duration)
        LoggingManager.log_warn("WindSensorWatcher.run(): Thread has been stopped")


    def stop(self):
        LoggingManager.log_info("WindSensorWatcher.stop(): Executing")
        self._stop_event.set()
        LoggingManager.log_info("WindSensorWatcher.stop(): Exiting")

