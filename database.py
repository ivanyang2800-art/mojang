import mysql.connector

class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ecommerce"
        )
        self.cursor = self.db.cursor()

    def create_user(self, username, password):
        sql = "INSERT INTO userdata (username, passuser) VALUES (%s, %s)"
        self.cursor.execute(sql, (username, password))
        self.db.commit()

    def check_user(self, username, password):
        sql = "SELECT userid, roleuser FROM userdata WHERE username=%s AND passuser=%s"
        self.cursor.execute(sql, (username, password))
        return self.cursor.fetchone()
