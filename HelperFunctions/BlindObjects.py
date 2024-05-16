from HighLevelControls.Managers.MessageManagers.Tables.BlindSettingsTable import BlindSettingsTable
from HighLevelControls.Managers.MessageManagers.Tables.DatabaseConnection import DatabaseConnection
from HighLevelControls.Managers.IndividualBlind import IndividualBlind
import HelperFunctions.Constants as Constants


ACTIVE_DICT = {}

@DatabaseConnection.DatabaseConnection
def initialize_blinds():
    BlindSettingsTable.create_table_if_not_exist()

    blind_table_dict = BlindSettingsTable.get_row(Constants.BLIND_ONE_KEY)
    blind_one = IndividualBlind(Constants.BLIND_ONE_KEY, Constants.blind_one, blind_table_dict[Constants.TIME_TO_MIDDLE], blind_table_dict[Constants.TIME_TO_BOTTOM])

    blind_table_dict = BlindSettingsTable.get_row(Constants.BLIND_TWO_KEY)
    blind_two = IndividualBlind(Constants.BLIND_TWO_KEY, Constants.blind_two, blind_table_dict[Constants.TIME_TO_MIDDLE], blind_table_dict[Constants.TIME_TO_BOTTOM])

    blind_table_dict = BlindSettingsTable.get_row(Constants.BLIND_THREE_KEY)
    blind_three = IndividualBlind(Constants.BLIND_THREE_KEY, Constants.blind_three, blind_table_dict[Constants.TIME_TO_MIDDLE], blind_table_dict[Constants.TIME_TO_BOTTOM])

    blind_table_dict = BlindSettingsTable.get_row(Constants.BLIND_FOUR_KEY)
    blind_four = IndividualBlind(Constants.BLIND_FOUR_KEY, Constants.blind_four, blind_table_dict[Constants.TIME_TO_MIDDLE], blind_table_dict[Constants.TIME_TO_BOTTOM])

    blind_table_dict = BlindSettingsTable.get_row(Constants.BLIND_FIVE_KEY)
    blind_five = IndividualBlind(Constants.BLIND_FIVE_KEY, Constants.blind_five, blind_table_dict[Constants.TIME_TO_MIDDLE], blind_table_dict[Constants.TIME_TO_BOTTOM])

    blind_table_dict = BlindSettingsTable.get_row(Constants.BLIND_SIX_KEY)
    blind_six =  IndividualBlind(Constants.BLIND_SIX_KEY, Constants.blind_six, blind_table_dict[Constants.TIME_TO_MIDDLE], blind_table_dict[Constants.TIME_TO_BOTTOM])

    blind_table_dict = BlindSettingsTable.get_row(Constants.BLIND_SEVEN_KEY)
    blind_seven = IndividualBlind(Constants.BLIND_SEVEN_KEY, Constants.blind_seven, blind_table_dict[Constants.TIME_TO_MIDDLE], blind_table_dict[Constants.TIME_TO_BOTTOM])

    blind_table_dict = BlindSettingsTable.get_row(Constants.BLIND_EIGHT_KEY)
    blind_eight = IndividualBlind(Constants.BLIND_EIGHT_KEY, Constants.blind_eight, blind_table_dict[Constants.TIME_TO_MIDDLE], blind_table_dict[Constants.TIME_TO_BOTTOM])

    #Starts out empty to begin with, but the dictionary persists even if the thread does not.
    return {
                 Constants.BLIND_ONE_KEY: blind_one,
                 Constants.BLIND_TWO_KEY: blind_two,
                 Constants.BLIND_THREE_KEY: blind_three,
                 Constants.BLIND_FOUR_KEY: blind_four,
                 Constants.BLIND_FIVE_KEY: blind_five,
                 Constants.BLIND_SIX_KEY: blind_six,
                 Constants.BLIND_SEVEN_KEY: blind_seven,
                 Constants.BLIND_EIGHT_KEY: blind_eight,
             }

BLIND_DICT = initialize_blinds()

