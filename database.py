import mysql.connector as konekdb

class database():
    def __init__(self):
        self.mydb=konekdb.connect(
            host="localhost",
            user="root",
            password="",
            database="ecommerce prologue"
        )
        self.cursor = self.mydb.cursor()

db_connection = database()