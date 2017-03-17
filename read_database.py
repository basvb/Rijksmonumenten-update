import pyodbc
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('data/config.ini')

db_file = 'data/Extract_ODB_{version}.mdb'.format(version='V10.2.11')
user = 'admin'
password = ''

print([x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')])
odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Wikipedia\Rijksmonumenten-update\data\Extract_ODB_V10.2.11.mdb'
conn = pyodbc.connect(odbc_conn_str)
cur = conn.cursor()

# run a query and get the results
SQL = 'SELECT * FROM mytable;' # your query goes here
rows = cur.execute(SQL).fetchall()
cur.close()
conn.close()