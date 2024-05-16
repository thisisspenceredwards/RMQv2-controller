"""
Format of message: TOPIC:METHOD=VARIABLE

Example: TOPIC:METHOD=VARIABLE,METHOD=VARIABLE TOPIC:METHOD=VARIABLE

split on whitespace

TOPIC:METHOD=VARIABLE,METHOD=VARIABLE

split on colon

TOPIC

METHOD=VARIABLE,METHOD=VARIABLE

split on comma

METHOD=VARIABLE

METHOD=VARIABLE

split on equals

METHOD
VARIABLE


"""

from HighLevelControls.Managers.LoggingManager import LoggingManager

class ParsedMessage:


    def __init__(self, topic, dictionary):
        self.topic = topic
        self.dictionary = dictionary


class Parser:


    @staticmethod
    def parse_message(message):
        LoggingManager.log_info("Parser.parseMessage(): Executing")
        message_arr = message.split()
        try:
            parsed_message_arr = []
            for message in message_arr:
                topic, message = message.split(":", 1)
                device_and_method = message.split(",")
                temp_dict = {}
                for entry in device_and_method:
                    device, method = entry.split("=", 1)
                    temp_dict[device] = method

                parsed_message_arr.append(ParsedMessage(topic, temp_dict))

            LoggingManager.log_info("Parser.parseMessage(): Exiting")
            return parsed_message_arr

        except Exception as e:
            LoggingManager.log_error(f"Parser.parseMessage(): Message was malformed {e}")
            return []
