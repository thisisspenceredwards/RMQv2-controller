def on_message(ch, method, properties, body):
    global channel, connection
    try:
        decoded_message = body.decode(Constants.ENCODING)
        uppercase_message = decoded_message.upper()
        parsed_message_arr = Parser.parse_message(uppercase_message)
        for parsed_message in parsed_message_arr:
            LoggingManager.log_info(f'RabbitMQ.on_message(): Topic received: {parsed_message.topic} Message received: {parsed_message.dictionary}')
            TopicManager.process_topic(parsed_message)
        LoggingManager.log_info("RabbitMQ.on_message(): Topic Handled")

    except Exception as e:
        LoggingManager.log_error(f"RabbitMQ.on_message(): {e}")
        catch_error_helper(e)


def create_channel():
    global channel
    channel = connection.channel()
    channel.exchange_declare(exchange = Constants.CONTROLLER_EXCHANGE, exchange_type = Constants.EXCHANGE_TYPE)
    channel.exchange_declare(exchange = Constants.CLIENT_EXCHANGE, exchange_type = Constants.EXCHANGE_TYPE)
    controller = channel.queue_declare(queue = "", exclusive = True)
    controller_queue_name = controller.method.queue
    channel.queue_bind(exchange= Constants.CONTROLLER_EXCHANGE, queue = controller_queue_name)
    channel.basic_consume(queue = controller_queue_name, auto_ack = True, on_message_callback = on_message)


def create_connection():
    global connection
    credentials = pika.PlainCredentials(Constants.USER_NAME, Constants.PASSWORD)
    parameters = pika.ConnectionParameters(Constants.IP_ADDRESS, Constants.PORT, Constants.VIRTUAL_BROKER, credentials, Constants.HEARTBEAT, blocked_connection_timeout = Constants.TIMEOUT)
    connection = pika.BlockingConnection(parameters)
    create_channel()
    NotificationManager.setup_connection(connection)


def set_blinds_to_top_position():
    LoggingManager.log_info("RabbitMQ.set_blind_to_top_position: Executing")
    try:
        Controller.turn_off_all_relays()
        Controller.set_blind_to_top_position()

    except Exception as e:
        LoggingManager.log_info(f"RabbitMQ.set_blind_to_top_position: Error {e}")

    LoggingManager.log_info("RabbitMQ.set_blind_to_top_position: Exiting")


import pika, time
from HighLevelControls.Managers.LoggingManager import LoggingManager
has_run_before = False

while(True):

    try:
        from HelperFunctions.Exceptions import catch_error_helper
        import HelperFunctions.Constants as Constants
        import HelperFunctions.SettingObjects as SO
        from HighLevelControls.Managers.NotificationManager import NotificationManager
        from HighLevelControls.Managers.TopicManager import TopicManager
        from HighLevelControls.Controller import Controller
        from HighLevelControls.Managers.MessageManagers.Tables.DatabaseConnection import DatabaseConnection
        from HighLevelControls.Parser import Parser, ParsedMessage
        from HighLevelControls.ThreadManager import ThreadManager
        from HighLevelControls.WatchdogManager import WatchdogManager
        from HighLevelControls.Managers.SweepWatcher import SweepWatcher
        from HighLevelControls.Managers.RelayBoardWatcher import RelayBoardWatcher
        from HighLevelControls.Managers.WindSensorWatcher import WindSensorWatcher
        from HighLevelControls.Managers.UPSWatcher import UPSWatcher
        from HighLevelControls.Managers.ConstantsManager import ConstantsManager
        from HighLevelControls.Managers.RelayManager import RelayManager
        import RPi.GPIO as GPIO

        GPIO.setmode(GPIO.BOARD)
        WatchdogManager.setup()
        SO.initialize_settings()

        channel = None
        connection = None
        create_connection()

        WatchdogManager.enable_watchdog()
        watchdog_thread_heart_beat = ThreadManager(WatchdogManager.send_heart_beat)
        watchdog_thread_heart_beat.start()
        watchdog_thread_timeout_watcher = ThreadManager(WatchdogManager.check_for_watchdog_timeout)
        watchdog_thread_timeout_watcher.start()

        relay_board_watcher = RelayBoardWatcher()
        relay_board_watcher.start()
        wind_sensor_watcher = WindSensorWatcher()
        wind_sensor_watcher.start()
        ups_watcher = UPSWatcher()
        ups_watcher.start()
        sweep_watcher = SweepWatcher()
        sweep_watcher.start()

        if not has_run_before:
            set_blinds_to_top_position()
        message = ConstantsManager.getInstance().current_values()
        channel.basic_publish(exchange = Constants.CLIENT_EXCHANGE, routing_key = '', body = message)

        has_run_before = True


        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            watchdog_thread_heart_beat.stop()
            watchdog_thread_timeout_watcher.stop()
            relay_board_watcher.stop()
            wind_sensor_watcher.stop()
            ups_watcher.stop()
            ups_watcher = None
            sweep_watcher.stop()
            sweep_watcher = None
            watchdog_thread_heart_beat = None
            watchdog_thread_timeout_watcher = None
            relay_board_watcher = None
            wind_sensor_watcher = None
            connection.close()
            GPIO.cleanup()
            break


    except Exception as e:
        LoggingManager.log_info(f'RabbitMQ.MAIN_LOOP: An Exception Occured -- {e}')
        channel.stop_consuming()
        watchdog_thread_heart_beat.stop()
        watchdog_thread_timeout_watcher.stop()
        relay_board_watcher.stop()
        wind_sensor_watcher.stop()
        ups_watcher.stop()
        ups_watcher = None
        sweep_watcher.stop()
        sweep_watcher = None
        watchdog_thread_heart_beat = None
        watchdog_thread_timeout_watcher = None
        relay_board_watcher = None
        wind_sensor_watcher = None
        connection.close()
        GPIO.cleanup()
        time.sleep(15)
        continue



