import psycopg2 as pg2
import sys
class Registre_IPs:

  def __init__(self,db_user,db_password,db_host,db_port,db_name,tableName):
    self.IPs = []
    self.db_user = db_user
    self.db_password = db_password
    self.db_host = db_host
    self.db_port = db_port
    self.db_name = db_name
    self.tableName = tableName
    self.actualitza()

  def __connecta__(self):
    try:
      connection = pg2.connect(user= self.db_user, password = self.db_password, host = self.db_host , port = self.db_port, database = self.db_name)
      return connection
    except Exception as error:
      raise Exception(error)  

  def getIPs(self):
    return self.IPs
  
  def actualitza(self):
    try:
      connection = self.__connecta__()
      with connection:
        cursor = connection.cursor()
        
        # safe query... no sql injection
        #cursor.execute(pg2.sql.SQL("select * from {}").format(pg2.sql.Identifier(self.db_name)))
        cursor.execute("select * from {}".format(self.tableName))

        ip_records = cursor.fetchall()
        self.IPs = []
        for row in ip_records:
          self.IPs.append(row[0])

    except Exception as error:
      raise Exception(error)

  # !!!! Si actualitza
  def borra(self):
    connection = self.__connecta__()
    try:
      with connection:
        cursor = connection.cursor()
        # safe query... no sql injection
        #cursor.execute("DELETE FROM {}".format(pg2.sql.Identifier(self.db_name)))
        cursor.execute("DELETE FROM {}".format(self.tableName))
	self.actualitza()
    except Exception as error:
      raise Exception( error)
        
    
    

