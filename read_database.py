import pyodbc
from configparser import ConfigParser


class MonumentsDatabase:
    def __init__(self):
        #Make a connection with the ODBC database, make sure to set the correct ODBC-connection in the config.ini
        config = ConfigParser()
        config.read('config.ini')
        odbc_conn_str = config.get('main', 'ODBC_connection_string')
        self.conn = pyodbc.connect(odbc_conn_str)
        self.cur = self.conn.cursor()

    def all_monuments(self):
        #Get a list of all monuments in the database by Rijksmonumentnumber
        SQL = 'SELECT OBJ_RIJKSNUMMER FROM OBJECT;' # your query goes here
        rows = self.cur.execute(SQL).fetchall()
        rows = [int(x[0]) for x in rows]
        return rows

    def close(self):
        self.cur.close()
        self.conn.close()
