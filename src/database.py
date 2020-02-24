from src.lib.mysql_connector import Connection
from src.lib import constants
from src.lib import password_encryptor as encrypt


class Database():
    def __init__(self):
        self.connection = Connection(constants.DB_HOST, constants.DB_NAME, constants.DB_USER, constants.DB_PASSWORD)

    def fetch_all_users(self):
        query = 'select * from users;'
        result = self.connection.execute_fetch_query(query)
        return result
    
    def insert_users_credentials(self, username, password):
        password = encrypt.encrypt_password(password)
        query = "insert into users values('{}', '{}')".format(username, password)
        self.connection.execute_insert_query(query)
    
    def insert_users_information(self, username, firstname, lastname):
        query = "insert into users_information values('{}', '{}', '{}')".format(username, firstname, lastname)
        self.connection.execute_insert_query(query)

    def fetch_user_details(self, username):
        query = "select firstname,lastname from users_information where username='{}'".format(username)
        result = self.connection.execute_fetch_query(query)[0]
        if result:
            return {'firstname': result[0], 'lastname': result[1]}
        else:
            return "User {} not registered.".format(username)
    
    def verify_login(self, username, password):
        query = "select password from users where username='{}'".format(username)
        result = self.connection.execute_fetch_query(query)

        if result and encrypt.check_encrypted_password(password, result[0][0]):
            return True
        else:
            return False
