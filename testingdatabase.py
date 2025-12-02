import mysql.connector as dbsql

class Jorky:
  def __init__(self):
    self.mydb = dbsql.connect(
      host="localhost",
      user="root",
      password="",
      database="ecommerce"
      )
    mycursor = self.mydb.cursor()  
    mycursor.execute("SHOW TABLES")

    for tb in mycursor:
      print(tb)
db = Jorky()
print(db.mydb)


