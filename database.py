import mysql.connector as dbsql

class database():
    def __init__(self):
        self.mydb=dbsql.connect(
            host="localhost",
            user="root",
            password="",
            database="ecommerce"
        )
        self.cursor = self.mydb.cursor()

db= database()
print(db.mydb)
