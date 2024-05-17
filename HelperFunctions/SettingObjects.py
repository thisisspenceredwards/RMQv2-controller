from HighLevelControls.Managers.MessageManagers.Tables.RoomSettingsTable import RoomSettingsTable
from HighLevelControls.Managers.MessageManagers.Tables.SweepSettingsTable import SweepSettingsTable
from HighLevelControls.Managers.MessageManagers.Tables.DatabaseConnection import DatabaseConnection
from HighLevelControls.Managers.IndividualBlind import IndividualBlind
import HelperFunctions.Constants as Constants

@DatabaseConnection.DatabaseConnection
def initialize_settings():
    RoomSettingsTable.create_table_if_not_exist()
    room_dict = RoomSettingsTable.get_settings()
    Constants.room_id.value = room_dict[Constants.ROOM_ID_KEY]
    Constants.WIND_SPEED_MAXIMUM_FOR_AUTO_RAISE_THRESHOLD = room_dict[Constants.WIND_SPEED_AUTO_RAISE_THRESHOLD_KEY]
    SweepSettingsTable.create_table_if_not_exist()
    sweep_dict = SweepSettingsTable.get_entries()
    Constants.SWEEP_DICT = sweep_dict

initialize_settings()
