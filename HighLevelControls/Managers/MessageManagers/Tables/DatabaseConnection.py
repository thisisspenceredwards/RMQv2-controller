import sqlite3
from HighLevelControls.Managers.LoggingManager import LoggingManager


class DatabaseConnection:

    _instance = None
    cursor = None
    connection = None

    @staticmethod
    def initialize_connection():
        LoggingManager.log_info("DatabaseConnection.initialize_connection(): Executing")
        if DatabaseConnection._instance is None:
            try:
                DatabaseConnection.connection = sqlite3.connect('Database.sqlite',timeout = 5)
                DatabaseConnection.connection.row_factory = sqlite3.Row
                DatabaseConnection._instance = DatabaseConnection()
            except sqlite3.Error as error:
                DatabaseConnection._instance = None
                LoggingManager.log_info(f"DatabaseConnection.initialize_connection(): Exiting, {error}")


    @staticmethod
    def initialize_cursor():
        LoggingManager.log_info("DatabaseConnection._initialize_cursor(): Executing")
        try:
            DatabaseConnection.initialize_connection()
            if DatabaseConnection.cursor is None:
                DatabaseConnection.cursor = DatabaseConnection.connection.cursor()
        except Exception as e:
            LoggingManager.log_error(f"DatabaseConnection._initialize_cursor: error -> {e}")


        LoggingManager.log_info("DatabaseConnection._initialize_cursor(): Exiting")

    @staticmethod
    def close_cursor():
        LoggingManager.log_info("DatabaseConnection.close_cursor(): Executing")
        DatabaseConnection.initialize_connection()
        DatabaseConnection.cursor.close()
        DatabaseConnection.cursor = None
        DatabaseConnection.connection.commit()
        LoggingManager.log_info("DatabaseConnection.close_cursor(): Exiting")


    #Decorator is put at the top level function call that then bookends the series of functions that uses the DB
    @staticmethod
    def DatabaseConnection(func):
        def wrapper(*args, **kwargs):
            DatabaseConnection.initialize_cursor()
            return_value = None
            try:
                return_value =  func(*args, **kwargs)
            except Exception as e:
                LoggingManager.log_error(f"DatabaseConnection.DatabaseConnection(): {e}")
            DatabaseConnection.close_cursor()
            return return_value
        return wrapper


