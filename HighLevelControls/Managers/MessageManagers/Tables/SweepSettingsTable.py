import sqlite3
import datetime
import HelperFunctions.Constants as Constants
import HelperFunctions.SettingsHelper as SH
from HighLevelControls.Managers.LoggingManager import LoggingManager
from HighLevelControls.Managers.MessageManagers.Tables.DatabaseConnection import DatabaseConnection

#This does not manage its connection to the DB directly.  You must use the DatabaseConnection class to open and close ideally using the nice decorator or the BlindTableManager
class SweepSettingsTable:

    SWEEP_TIME = "SWEEP_TIME"
    _init_query = SH.SWEEP_SETTINGS_CREATE_TABLE
    _select_query = SH.SWEEP_SETTINGS_SELECT
    _select_sweep_time = SH.SWEEP_SETTINGS_SELECT_SWEEP_TIME
    _insert_query = SH.SWEEP_SETTINGS_INSERT
    _delete_query = SH.SWEEP_SETTINGS_DROP_TABLE
    _remove_row_query = SH.SWEEP_SETTINGS_REMOVE_ROW
    _check_number_of_rows = SH.SWEEP_SETTINGS_CHECK_NUMBER_OF_ROWS
    _check_if_entry_exists = SH.SWEEP_SETTINGS_CHECK_IF_ENTRY_EXISTS


    @staticmethod
    def create_table_if_not_exist():
        LoggingManager.log_info("SweepSettingsTable.create_table(): Executing")
        try:
            #fails if DB doesn't exist
            SweepSettingsTable.get_number_of_rows()

        except Exception as e:
            LoggingManager.log_info(f"SweepSettingsTable.create_table(): error {e}")
            DatabaseConnection.cursor.execute(SweepSettingsTable._init_query)
            LoggingManager.log_info("SweepSettingsTable: Opened database successfully")

        LoggingManager.log_info("SweepSettingsTable.create_table(): Exiting")


    @staticmethod
    def get_entries():
        LoggingManager.log_info("SweepSettingsTable.get_entries(): Executing")
        rows = DatabaseConnection.cursor.execute(SweepSettingsTable._select_query).fetchall()
        entries_dict = {}
        for row in rows:
           sweep = row[SweepSettingsTable.SWEEP_TIME]
           key = SweepSettingsTable.get_controller_readable_sweep_time(sweep)
           entries_dict[key] = sweep

        LoggingManager.log_info("SweepSettingsTable.get_entries(): Exiting")
        return entries_dict



    @staticmethod
    def get_number_of_rows():
        LoggingManager.log_info("SweepSettingsTable.get_number_of_rows(): Executing")
        try:
            number = DatabaseConnection.cursor.execute(SweepSettingsTable._check_number_of_rows).fetchone()[0]
            LoggingManager.log_info("SweepSettingsTable.get_number_of_rows(): Exiting")
            return number
        except Exception as e:
            raise sqlite3.Error(f'SweepSettingsTable.get_number_of_rows(): Failed {e}')

    @staticmethod
    def insert(val):
        LoggingManager.log_info("SweepSettingsTable.insert(): Executing")

        readable_time, time_in_seconds = val.split("^")
        time = time_in_seconds.split(".")
        sweep = time[0]
        int_sweep = int(sweep) #used to get controller readable time, here to abort adding to db if it fails

        DatabaseConnection.cursor.execute(SweepSettingsTable._insert_query, (readable_time, sweep))
        database_sweep = DatabaseConnection.cursor.execute(SweepSettingsTable._check_if_entry_exists, (sweep, )).fetchone()[0]
        if database_sweep == sweep: #successfully added to the database
            key = SweepSettingsTable.get_controller_readable_sweep_time(int_sweep)
            Constants.SWEEP_DICT[key] = sweep

        LoggingManager.log_info("SweepSettingsTable.insert(): Executing")


    @staticmethod
    def delete(val):
        LoggingManager.log_info("SweepSettingsTable.delete(): Executing")
        sweep = DatabaseConnection.cursor.execute(SweepSettingsTable._select_sweep_time, (val,)).fetchone()
        controller_readable_sweep_time = SweepSettingsTable.get_controller_readable_sweep_time(sweep[SweepSettingsTable.SWEEP_TIME])
        DatabaseConnection.cursor.execute(SweepSettingsTable._remove_row_query, (val,))
        Constants.SWEEP_DICT.pop(controller_readable_sweep_time)
        LoggingManager.log_info("SweepSettingsTable.delete(): Exiting")


    @staticmethod
    def get_controller_readable_sweep_time(time_in_seconds):
        time = datetime.datetime.fromtimestamp(int(time_in_seconds))
        return time.strftime("%H:%M")
