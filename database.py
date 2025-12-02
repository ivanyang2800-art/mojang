import mysql.connector as dbsql

class Database:
    def __init__(self):
        self.mydb = dbsql.connect(
            host="localhost",
            user="root",
            password="",
            database="ecommerce"
            )
        self.cursor = self.mydb.cursor()
        def get_data(self, query):
            self.cursor.execute(query)
            return self.cursor.fetchall()


        def process_data_query(self, query):
            self.cursor.execute(query)
            self.mydb.commit()
            return True
        
db_connection = Database()
