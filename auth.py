from database import db_connection

class Auth:
    def __init__(self):
        self.user_id = ""
        self.user_name = ""

    def proses_login(self, username, password) :
        db_connection.cursor.execute(f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'")
        user = db_connection.cursor.fetchall()
        return user