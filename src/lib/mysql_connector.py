import mysql.connector
from mysql.connector import Error


class Connection:
    def __init__(self, host, database, user, password):
        self.db_host = host
        self.database_name = database
        self.db_user = user
        self.db_password = password
        self._connect()

    def _connect(self):
        try:
            self.connection = mysql.connector.connect(host=self.db_host,
                                                      database=self.database_name,
                                                      user=self.db_user,
                                                      password=self.db_password)
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_info)
        except Error as e:
            print("Error while connecting to MySQL", e)

    def execute_fetch_query(self, query):
        if self.connection.is_connected():
            try:
                cursor = self.connection.cursor(buffered=True)
                cursor.execute(query)
                self.connection.commit()
                result = cursor.fetchall()
                cursor.close()
                return result
            except Exception as e:
                raise Exception("Failed to execute fetch query - '{}', due to following error : \n{}".format(query, e))
        else:
            raise Exception("Connection to the database {} not established".format(self.database_name))

    def execute_insert_query(self, query):
        if self.connection.is_connected():
            try:
                cursor = self.connection.cursor(buffered=True)
                cursor.execute(query)
                self.connection.commit()
                cursor.close()
            except Exception as e:
                raise Exception("Failed to execute insert query - '{}', due to following error : \n{}".format(query, e))
        else:
            raise Exception("Connection to the database {} not established".format(self.database_name))

    def __del__(self):
        if self.connection.is_connected():
            print("Closing database connection....")
            self.connection.close()
        else:
            print("Database connection already closed")
