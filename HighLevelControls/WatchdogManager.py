import os
import RPi.GPIO as GPIO
from HighLevelControls.Managers.LoggingManager import LoggingManager

class WatchdogManager:

    GPIO.setmode(GPIO.BOARD)
    _enable_watchdog_pin = 31 #GPIO6
    _heart_beat_pin = 29 #GPIO5
    _watchdog_timeout_pin = 32 #GPIO12
    _signal_shutdown_pin = 36 #GPIO16


    @staticmethod
    def setup():
        GPIO.setup(WatchdogManager._enable_watchdog_pin, GPIO.OUT)
        GPIO.setup(WatchdogManager._heart_beat_pin, GPIO.OUT)
        GPIO.setup(WatchdogManager._watchdog_timeout_pin, GPIO.IN)
        GPIO.setup(WatchdogManager._signal_shutdown_pin, GPIO.OUT)


    @staticmethod
    def enable_watchdog():
        LoggingManager.log_info("WatchdogManager.enable_watchdog: Executing")
        GPIO.output(WatchdogManager._enable_watchdog_pin, GPIO.HIGH)
        LoggingManager.log_info("WatchdogManager.enable_watchdog: Exiting")


    @staticmethod
    def send_heart_beat():
        LoggingManager.log_info("WatchdogManager.send_heart_beat: Executing")
        if GPIO.input(WatchdogManager._heart_beat_pin) == 1:
            GPIO.output(WatchdogManager._heart_beat_pin, GPIO.LOW)
        else:
            GPIO.output(WatchdogManager._heart_beat_pin, GPIO.HIGH)
        LoggingManager.log_info("WatchdogManager.send_heart_beat: Exiting")


    @staticmethod
    def _shut_down():
        LoggingManager.log_info("WatchdogManager.shut_down: Executing")
        os.system("sudo systemctl start reboot.target")
        LoggingManager.log_info("WatchdogManager.shut_down: Exiting")


    @staticmethod
    def check_for_watchdog_timeout():
        LoggingManager.log_info("WatchdogManager.check_for_watchdog_timeout: Executing")
        if GPIO.input(WatchdogManager._watchdog_timeout_pin) == 1:
            WatchdogManager._shut_down()

        LoggingManager.log_info("WatchdogManager.check_for_watchdog_timeout: Exiting")

