import mysql.connector

class Database():
    def __init__(self):    
        self.mydb= mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="ecommerce_simple"
        )

        self.cursor=self.mydb.cursor()

        


    def get_data(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    

    def process_data_query(self, query, params=None):
        self.cursor.execute(query, params)
        self.mydb.commit()
        return True
