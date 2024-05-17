import sqlite3
import HelperFunctions.Constants as Constants
import HelperFunctions.SettingsHelper as SH
from HighLevelControls.Managers.LoggingManager import LoggingManager
from HighLevelControls.Managers.MessageManagers.Tables.DatabaseConnection import DatabaseConnection

class RoomSettingsTable:


    _ID = 1
    _init_query = SH.ROOM_SETTINGS_CREATE_TABLE
    _select_query = SH.ROOM_SETTINGS_SELECT
    _insert_query = SH.ROOM_SETTINGS_INSERT
    _update_wind_speed_auto_raise_threshold_query = SH.ROOM_SETTINGS_UPDATE_WIND_SPEED_AUTO_RAISE_THRESHOLD
    _update_wind_speed_lower_lock_threshold_query = SH.ROOM_SETTINGS_UPDATE_WIND_SPEED_LOWER_LOCK_THRESHOLD
    _update_room_id_query = SH.ROOM_SETTINGS_UPDATE_ROOM_ID
    _delete_query = SH.ROOM_SETTINGS_DELETE
    _check_number_of_rows = SH.ROOM_SETTINGS_CHECK_NUMBER_OF_ROWS


    @staticmethod
    def _populate_table():
        LoggingManager.log_info("RoomSettingsTable._populate_table(): Executing")
        #insert queries
        statement = (
            int(RoomSettingsTable._ID),
            str(Constants.MAC_ADDRESS),
            float(Constants.WIND_SPEED_MAXIMUM_FOR_AUTO_RAISE_THRESHOLD),
            float(Constants.WIND_SPEED_MAXIMUM_FOR_AUTO_RAISE_THRESHOLD)
        )
        DatabaseConnection.cursor.execute(RoomSettingsTable._insert_query, statement)

        LoggingManager.log_info("RoomSettingsTable._populate_table(): Exiting")


    @staticmethod
    def get_number_of_rows():
        LoggingManager.log_info("RoomSettingsTable.get_number_of_rows(): Executing")
        try:
            number = DatabaseConnection.cursor.execute(RoomSettingsTable._check_number_of_rows).fetchone()[0]
            LoggingManager.log_info("RoomSettingsTable.get_number_of_rows(): Exiting")
            return number
        except Exception as e:
            raise sqlite3.Error(f'RoomSettingsTable.get_number_of_rows(): Failed {e}')


    @staticmethod
    def create_table_if_not_exist():
        LoggingManager.log_info("RoomSettingsTable.create_table(): Executing")
        try:
            #fails if DB doesn't exist
            number = RoomSettingsTable.get_number_of_rows()
            if number != SH.NUMBER_OF_ROOM_SETTING_ENTRIES:
                DatabaseConnection.cursor.execute(RoomSettingsTable._delete_query)
                raise Exception("Incorrect number of room entries, remaking table")
        except:
            LoggingManager.log_info("RoomSettingsTable.create_table(): Table doesn't exist, creating and populating")
            DatabaseConnection.cursor.execute(RoomSettingsTable._init_query)
            RoomSettingsTable._populate_table()
            LoggingManager.log_info("RoomSettingsTable: Opened database successfully")

        LoggingManager.log_info("RoomSettingsTable.create_table(): Exiting")


    @staticmethod
    def get_settings():
        LoggingManager.log_info("RoomSettingsTable.get_settings(): Executing")
        row = DatabaseConnection.cursor.execute(RoomSettingsTable._select_query).fetchone()
        LoggingManager.log_info("RoomSettingsTable.get_settings(): Exiting")
        return {Constants.ROOM_ID_KEY: row[Constants.ROOM_ID_KEY], Constants.WIND_SPEED_AUTO_RAISE_THRESHOLD_KEY: row[Constants.WIND_SPEED_AUTO_RAISE_THRESHOLD_KEY]}


    @staticmethod
    def update_wind_speed_auto_raise_threshold(wind_threshold):
        LoggingManager.log_info("RoomSettingsTable.update_wind_speed_auto_raise_threshold(): Executing")
        entities = (wind_threshold,)
        DatabaseConnection.cursor.execute(RoomSettingsTable._update_wind_speed_auto_raise_threshold_query, entities)
        LoggingManager.log_info("RoomSettingsTable.update_wind_speed_auto_raise_threshold(): Exiting")

    @staticmethod
    def update_wind_speed_lower_lock_threshold(wind_threshold):
        LoggingManager.log_info("RoomSettingsTable.update_wind_speed_lower_lock_threshold(): Executing")
        entities = (wind_threshold,)
        DatabaseConnection.cursor.execute(RoomSettingsTable._update_wind_speed_lower_lock_threshold_query, entities)
        LoggingManager.log_info("RoomSettingsTable.update_wind_speed_lower_lock_threshold(): Exiting")

    @staticmethod
    def update_room_id(room_id):
        LoggingManager.log_info("RoomSettingsTable.WIND_SENSOR_UPDATE_WIND_SPEED_AUTO_RAISE_THRESHOLD(): Executing")
        entities = (room_id,)
        DatabaseConnection.cursor.execute(RoomSettingsTable._update_room_id_query, entities)
        LoggingManager.log_info("RoomSettingsTable.WIND_SENSOR_UPDATE_WIND_SPEED_AUTO_RAISE_THRESHOLD(): Exiting")

