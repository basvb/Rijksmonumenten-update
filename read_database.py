import pyodbc
import json
from urllib.request import urlopen
from configparser import ConfigParser
import pickle
import RD_to_WGS84 as cc

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
        SQL = 'SELECT OBJ_RIJKSNUMMER FROM OBJECT;'
        rows = self.cur.execute(SQL).fetchall()
        rows = [int(x[0]) for x in rows]
        return rows

    def understand_database(self):
        tables = list(self.cur.tables())

        print('tables')
        for b in tables:
            print(b)
        tables = ['tblOBJECT', 'tblOBJECTBOUWACTIVITEIT', 'tblOBJECTFUNCTIE', 'tblOBJECTADRES', 'tblTEXT_OBJECT']
        for tab in tables:
            for row in self.cur.columns(table=tab):
                print("Field name: " + str(row.column_name) + ' (' + tab + ')')

    def monument_as_rowtemplate(self, rm_id):
        SQL_object = 'SELECT OBJ_X_COORD, OBJ_Y_COORD, OBJ_CBSCODE_ZKP, PLA_NAAM, OBJ_RIJKSNUMMER, OBJ_NAAM, OBJ_WETSARTIKEL_ZKP FROM tblOBJECT WHERE OBJ_RIJKSNUMMER={id};'.format(id=rm_id)
        SQL_objectadres ='SELECT * FROM tblOBJECTADRES WHERE OBJ_NUMMER={id};'.format(id=rm_id)
        SQL_objectbeschrijving ='SELECT * FROM tblTEXT_OBJECT WHERE OBJ_NUMMER={id};'.format(id=rm_id)

        rijksmonument = self.cur.execute(SQL_object).fetchall()
        adres = self.cur.execute(SQL_objectadres).fetchall()
        print(rijksmonument)
        print(adres)

        '''
        <!---->
        {{Tabelrij rijksmonument|woonplaats=Bennekom|objectnaam=De Harn
        |type_obj=G|oorspr_functie=Boerderij|cbs_tekst=Agrarische gebouwen
        |bouwjaar={{Sorteer|1500|16e eeuw}}|architect=|adres=Harnsedijkje 2A
        |lat=52.00194|lon=5.64909|objrijksnr=14453|image=De Harn.jpg|commonscat=De Harn, Bennekom}}
        '''


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
        self.monuments = monuments

    def save_monuments_to_file(self, filename='WikipediaMonumentsDatabase'):
        if self.monuments is not None:
            save_obj(self.monuments, filename)
            return True
        else:
            return False

    def load_monuments_from_file(self, filename='WikipediaMonumentsDatabase'):
        #TODO: test whether file exists
        self.from_file=True
        return load_obj(filename)

    def all_monuments(self):
        if self.monuments is None:
            return False
        return [int(x['id']) for x in self.monuments]
