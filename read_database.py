import pyodbc
import json
from urllib.request import urlopen
from configparser import ConfigParser
import pickle


def save_obj(obj, name ):
    with open('data/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('data/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

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
    def __init__(self, from_file=False, filename='WikipediaMonumentsDatabase'):
        if from_file is False:
            self.from_file = False
            self.monuments = None
        else:
            self.from_file = True
            self.monuments = self.load_monuments_from_file(filename)

    def load_monuments_from_web(self):
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
            if counter is 3:
                break
            counter += 1
        self.monuments = monuments

    def save_monuments_to_file(self, filename='WikipediaMonumentsDatabase'):
        if self.monuments is not None:
            save_obj(self.monuments, filename)
            return True
        else:
            return False

    def load_monuments_from_file(self, filename='WikipediaMonumentsDatabase'):
        #TODO: test whether file exists
        return load_obj(filename)


