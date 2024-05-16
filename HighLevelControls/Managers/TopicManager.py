import HelperFunctions.Constants as Constants
from HighLevelControls.Managers.LoggingManager import LoggingManager
from HighLevelControls.Managers.NotificationManager import NotificationManager
from HighLevelControls.Managers.MessageManagers.BlindSettingsManager import BlindSettingsManager
from HighLevelControls.Managers.MessageManagers.RoomSettingsManager import RoomSettingsManager
from HighLevelControls.Managers.MessageManagers.ClassroomManager import ClassroomManager
from HighLevelControls.Managers.MessageManagers.ShutDownManager import ShutDownManager
class TopicManager:

    #Methods in the topic_dictionary MUST have a 'process_message' function, this was enforced but decorators complicated it
    _topic_dictionary = { Constants.MQTT_TOPIC_CLASSROOM: ClassroomManager,
                           Constants.MQTT_TOPIC_NOTIFICATIONS: NotificationManager,
                            Constants.MQTT_TOPIC_BLIND_SETTINGS: BlindSettingsManager,
                             Constants.MQTT_TOPIC_ROOM_SETTINGS: RoomSettingsManager,
                              Constants.MQTT_TOPIC_SHUT_DOWN_SETTINGS: ShutDownManager
                        }
    @staticmethod
    def process_topic(parsed_message):
        topic = parsed_message.topic
        LoggingManager.log_info(f'TopicManager.process_topic(): Topic is {topic}')
        if topic in TopicManager._topic_dictionary:
            entry = TopicManager._topic_dictionary.get(topic)()
            entry.process_message(parsed_message)
        else:
            LoggingManager.log_error("TopicManager.process_topic(): topic is not contained in dictionary.")

        LoggingManager.log_info("TopicManager.process_topic(): Exiting")
