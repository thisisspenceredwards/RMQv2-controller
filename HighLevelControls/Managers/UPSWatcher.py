import time
import threading
import RPi.GPIO as GPIO
from HighLevelControls.Managers.LoggingManager import LoggingManager

class UPSWatcher(threading.Thread):


    _SHUTDOWN_PIN = 36
    _UPS_GPIO_PIN = 37
    _consecutive_instances_on_battery_power = 0


    def __init__(self, sleep_duration = 5):
        LoggingManager.log_info("UPSWatcher.init(): Called")
        threading.Thread.__init__(self)
        self.sleep_duration = sleep_duration
        self._stop_event = threading.Event()
        GPIO.setup(UPSWatcher._UPS_GPIO_PIN, GPIO.IN)
        GPIO.setup(UPSWatcher._SHUTDOWN_PIN, GPIO.OUT)
        LoggingManager.log_info("UPSWatcher.init(): Complete")


    def run(self):
        LoggingManager.log_info("UPSWatcher.run(): Starting")
        while not self._stop_event.isSet():
            LoggingManager.log_info("UPSWatcher.run(): Executing")
            UPSWatcher._check_ups_gpio_pin()
            time.sleep(self.sleep_duration)
        LoggingManager.log_warn("UPSWatcher.run(): Thread has been stopped")

    def stop(self):
        LoggingManager.log_info("UPSWatcher.stop(): Executing")
        self._stop_event.set()
        LoggingManager.log_info("UPSWatcher.stop(): Exiting")


    @staticmethod
    def _check_ups_gpio_pin():
        LoggingManager.log_info("UPSWatcher.run(): Starting")
        if GPIO.input(UPSWatcher._UPS_GPIO_PIN) == 1:
            UPSWatcher._consecutive_instances_on_battery_power += 1

        else: #Device has line power
            UPSWatcher._consecutive_instances_on_battery_power = 0

        if UPSWatcher._consecutive_instances_on_battery_power >= 12:  #spent a total of 60 seconds with no external power
            LoggingManager.log_info("UPSWatcher.run(): Currently on battery power")
            UPSWatcher._shut_down()

        LoggingManager.log_info("UPSWatcher._check_ups_gpio_pin(): Exiting")


    @staticmethod
    def _shut_down():
        LoggingManager.log_info("UPSWatcher._shut_down(): Executing")
        GPIO.output(UPSWatcher._SHUTDOWN_PIN, GPIO.HIGH)
