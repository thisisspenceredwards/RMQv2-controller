import sqlite3
import HelperFunctions.Constants as Constants
import HelperFunctions.SettingsHelper as SH
from HighLevelControls.Managers.LoggingManager import LoggingManager
from HighLevelControls.Managers.MessageManagers.Tables.DatabaseConnection import DatabaseConnection

#This does not manage its connection to the DB directly.  You must use the DatabaseConnection class to open and close ideally using the nice decorator or the BlindTableManager
class BlindSettingsTable:


    _init_query = SH.BLIND_SETTINGS_CREATE_TABLE
    _select_row = SH.BLIND_SETTINGS_SELECT
    _select_time_to_middle_query = SH.BLIND_SETTINGS_SELECT_TIME_TO_MIDDLE
    _select_time_to_bottom_query = SH.BLIND_SETTINGS_SELECT_TIME_TO_BOTTOM
    _insert_query = SH.BLIND_SETTINGS_INSERT
    _update_query = SH.BLIND_SETTINGS_UPDATE
    _delete_query = SH.BLIND_SETTINGS_DELETE
    _check_number_of_rows = SH.BLIND_SETTINGS_CHECK_NUMBER_OF_ROWS


    @staticmethod
    def get_row(blind_id):
        row = DatabaseConnection.cursor.execute(BlindSettingsTable._select_row, (blind_id, )).fetchone()
        return {Constants.TIME_TO_MIDDLE: row[Constants.TIME_TO_MIDDLE], Constants.TIME_TO_BOTTOM: row[Constants.TIME_TO_BOTTOM]}


    @staticmethod
    def _populate_table():
        LoggingManager.log_info("BlindSettingsTable._populate_table(): Executing")
        #insert queries
        blind_one = (Constants.BLIND_ONE_KEY, Constants.BLIND_LOCATION_MIDDLE, Constants.BLIND_LOCATION_BOTTOM)
        blind_two = (Constants.BLIND_TWO_KEY, Constants.BLIND_LOCATION_MIDDLE, Constants.BLIND_LOCATION_BOTTOM)
        blind_three = (Constants.BLIND_THREE_KEY, Constants.BLIND_LOCATION_MIDDLE, Constants.BLIND_LOCATION_BOTTOM)
        blind_four = (Constants.BLIND_FOUR_KEY, Constants.BLIND_LOCATION_MIDDLE, Constants.BLIND_LOCATION_BOTTOM)
        blind_five = (Constants.BLIND_FIVE_KEY, Constants.BLIND_LOCATION_MIDDLE, Constants.BLIND_LOCATION_BOTTOM)
        blind_six = (Constants.BLIND_SIX_KEY, Constants.BLIND_LOCATION_MIDDLE, Constants.BLIND_LOCATION_BOTTOM)
        blind_seven = (Constants.BLIND_SEVEN_KEY, Constants.BLIND_LOCATION_MIDDLE, Constants.BLIND_LOCATION_BOTTOM)
        blind_eight = (Constants.BLIND_EIGHT_KEY, Constants.BLIND_LOCATION_MIDDLE, Constants.BLIND_LOCATION_BOTTOM)
        DatabaseConnection.cursor.execute(BlindSettingsTable._insert_query, blind_one)
        DatabaseConnection.cursor.execute(BlindSettingsTable._insert_query, blind_two)
        DatabaseConnection.cursor.execute(BlindSettingsTable._insert_query, blind_three)
        DatabaseConnection.cursor.execute(BlindSettingsTable._insert_query, blind_four)
        DatabaseConnection.cursor.execute(BlindSettingsTable._insert_query, blind_five)
        DatabaseConnection.cursor.execute(BlindSettingsTable._insert_query, blind_six)
        DatabaseConnection.cursor.execute(BlindSettingsTable._insert_query, blind_seven)
        DatabaseConnection.cursor.execute(BlindSettingsTable._insert_query, blind_eight)
        LoggingManager.log_info("BlindSettingsTable._populate_table(): Exiting")


    @staticmethod
    def get_number_of_rows():
        LoggingManager.log_info("BlindSettingsTable.get_number_of_rows(): Executing")
        try:
            number = DatabaseConnection.cursor.execute(BlindSettingsTable._check_number_of_rows).fetchone()[0]
            LoggingManager.log_info("BlindSettingsTable.get_number_of_rows(): Exiting")
            return number
        except Exception as e:
            raise sqlite3.Error(f'BlindSettingsTable.get_number_of_rows(): Failed {e}')


    @staticmethod
    def create_table_if_not_exist():
        LoggingManager.log_info("BlindSettingsTable.create_table(): Executing")
        try:
            #fails if DB doesn't exist
            number = BlindSettingsTable.get_number_of_rows()
            if number != SH.NUMBER_OF_BLIND_ENTRIES:
                raise Exception("Wrong number of entries")

        except Exception as e:
            LoggingManager.log_info(f"BlindSettingsTable.create_table(): error {e}")
            DatabaseConnection.cursor.execute(BlindSettingsTable._init_query)
            BlindSettingsTable._populate_table()
            LoggingManager.log_info("BlindSettingsTable: Opened database successfully")

        LoggingManager.log_info("BlindSettingsTable.create_table(): Exiting")


    @staticmethod
    def get_time_to_middle(blind_id):
        LoggingManager.log_info("BlindSettingsTable.get_time_to_middle(): Executing")
        row = DatabaseConnection.cursor.execute(BlindSettingsTable._select_time_to_middle_query, (blind_id, )).fetchone()
        LoggingManager.log_info("BlindSettingsTable.get_time_to_middle(): Exiting")
        return row[Constants.TIME_TO_MIDDLE]


    @staticmethod
    def get_time_to_bottom(blind_id):
        LoggingManager.log_info("BlindSettingsTable.get_time_to_bottom(): Executing")
        row = DatabaseConnection.cursor.execute(BlindSettingsTable._select_time_to_bottom_query, (blind_id, )).fetchone()
        LoggingManager.log_info("BlindSettingsTable.get_time_to_bottom(): Exiting")
        return row[Constants.TIME_TO_BOTTOM]


    @staticmethod
    def update_entry(blind_id, time_to_middle = None, time_to_bottom = None):
        LoggingManager.log_info("BlindSettingsTable.update_entry(): Executing")
        try:
            if time_to_middle is None:
                time_to_middle = BlindSettingsTable.get_time_to_middle(blind_id)

            if time_to_bottom is None:
                time_to_bottom = BlindSettingsTable.get_time_to_bottom(blind_id)

            entities = (float(time_to_middle), float(time_to_bottom), blind_id)
            DatabaseConnection.cursor.execute(BlindSettingsTable._update_query, entities)
        except Exception as e:
            LoggingManager.log_error(f"BlindSettingsTable.update_entry(): error {e}")

        LoggingManager.log_info("BlindSettingsTable.update_entry(): Exiting")
