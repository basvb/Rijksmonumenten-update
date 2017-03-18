import pyodbc
import json
from urllib.request import urlopen
from configparser import ConfigParser


class RCEMonumentsDatabase:
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
        rows = [x[0] for x in rows]
        return rows

    def close(self):
        self.cur.close()
        self.conn.close()

class WikipediaMonumentsDatabase:
    def __init__(self):
        None
    def all_monuments(self):
        #Get a list of all monuments in the database by Rijksmonumentnumber
        base_url = 'https://tools.wmflabs.org/heritage/api/api.php?action=search&srcountry=nl&srlang=nl&format=json'
        all_monuments=False
        counter = 0
        url = base_url
        monuments = []
        while not all_monuments:
            response = urlopen(url)
            data = json.loads(response.read().decode("utf-8"))
            monuments = monuments + data['monuments']
            if 'continue' in data:
                url = base_url + '&srcontinue=' + data['continue']['srcontinue']
            else:
                break
            #Temporary break to avoid endless loops and speedtest
            if counter==3:
                break
            counter+=1
        print(monuments)
        print(len(monuments))