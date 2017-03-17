import pyodbc
from configparser import ConfigParser

#Make a connection with the ODBC database, make sure to set the correct ODBC-connection in the config.ini
config = ConfigParser()
config.read('config.ini')
odbc_conn_str = config.get('main', 'ODBC_connection_string')
conn = pyodbc.connect(odbc_conn_str)
cur = conn.cursor()

# run a query and get the results
SQL = 'SELECT OBJ_RIJKSNUMMER FROM OBJECT;' # your query goes here
rows = cur.execute(SQL).fetchall()
print(len(rows))
cur.close()
conn.close()