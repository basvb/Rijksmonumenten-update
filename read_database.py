import pyodbc
import json
from urllib.request import urlopen
from configparser import ConfigParser
import pickle
import RD_to_WGS84

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
        SQL = 'SELECT OBJ_RIJKSNUMMER FROM tblOBJECT;'
        rows = self.cur.execute(SQL).fetchall()
        rows = [int(x[0]) for x in rows]
        return rows

    def understand_database(self):
        tables = list(self.cur.tables())

        print('tables')
        for b in tables:
            print(b)
        tables = ['tblOBJECT', 'tblOBJECTBOUWACTIVITEIT', 'tblOBJECTFUNCTIE', 'tblOBJECTADRES', 'tblTEXT_OBJECT', 'tblOBJECTFUNCTIE']
        for tab in tables:
            for row in self.cur.columns(table=tab):
                print("Field name: " + str(row.column_name) + ' (' + tab + ')')

    def get_rce_information_on_monument(self, rm_id):
        #Determine the object number used in the database, if it can not be found return nothing/False
        try:
            obj_nummer= self.cur.execute('SELECT OBJ_NUMMER FROM tblOBJECT WHERE OBJ_RIJKSNUMMER={id};'.format(id=rm_id)).fetchall()[0][0]
        except IndexError:
            print(rm_id)
            return False

        #All queries which will be used to determine the relevant info to build a rowtemplate from
        SQL_object = 'SELECT OBJ_NUMMER, COM_RIJKSNUMMER, OBJ_X_COORD, OBJ_Y_COORD, OBJ_CBSCODE_ZKP, OBJ_RIJKSNUMMER, OBJ_NAAM, OBJ_WETSARTIKEL_ZKP FROM tblOBJECT WHERE OBJ_RIJKSNUMMER={id};'.format(id=rm_id)
        SQL_objectadres ='SELECT OAD_STRAAT, OAD_HUISNUMMER, OAD_TOEVOEGING, OAD_PLA_NAAM_CAP FROM tblOBJECTADRES WHERE OBJ_NUMMER={obj};'.format(obj=obj_nummer)
        SQL_objectbeschrijving ='SELECT TXO_TEKST FROM tblTEXT_OBJECT WHERE OBJ_NUMMER={obj};'.format(obj=obj_nummer)
        SQL_objectfunctie ='SELECT CAS_OMSCHRIJVING, OFU_IND_OORSPHUIDIG_ZKP FROM tblOBJECTFUNCTIE WHERE OBJ_NUMMER={obj};'.format(obj=obj_nummer)
        SQL_objectbouwactiviteit ='SELECT * FROM tblOBJECTBOUWACTIVITEIT WHERE OBJ_NUMMER={obj};'.format(obj=obj_nummer)
        SQL_objectambacht ='SELECT * FROM tblOBJECTAMBACHT WHERE OBJ_NUMMER={obj};'.format(obj=obj_nummer)

        #The results from the queries above after execution
        res_object = self.cur.execute(SQL_object).fetchall()
        res_objectadres = self.cur.execute(SQL_objectadres).fetchall()
        res_objectbeschrijving = self.cur.execute(SQL_objectbeschrijving).fetchall()
        res_objectfunctie = self.cur.execute(SQL_objectfunctie).fetchall()
        res_objectbouwactiviteit = self.cur.execute(SQL_objectbouwactiviteit).fetchall()
        res_objectambacht = self.cur.execute(SQL_objectambacht).fetchall()

        #TODO: remove in final versions
        print(res_object)
        print(res_objectadres)
        print(res_objectbeschrijving)
        print(res_objectfunctie)
        print(res_objectbouwactiviteit)
        print(res_objectambacht)


        #The city/place in which the object is located. Sometimes this is all uppercase so an attempt to fix that is done.
        woonplaats = res_objectadres[0][3]
        if woonplaats.isupper():
            woonplaats = woonplaats.lower().title()

        #Here the address of the object is determined and cleaned.
        if res_objectadres[0][1] is None:
            adres = res_objectadres[0][0]
        elif res_objectadres[0][2] is None:
            adres = res_objectadres[0][0] + ' ' + str(res_objectadres[0][1])
        else:
            adres = res_objectadres[0][0] + ' ' + str(res_objectadres[0][1]) + str(res_objectadres[0][2])
        if adres == 'N.v.t.':
            adres=''

        #Here either the object name or description is determined. The description needs manual clean up later on.
        if res_object[0][6] is not None:
            objectnaam = res_object[0][6]
        elif res_objectbeschrijving[0][0] is not None:
            objectnaam = res_objectbeschrijving[0][0][0:200]
        else:
            objectnaam = ''

        #The object function is determined.
        if res_objectfunctie == []:
            oorspr_functie = ''
        elif res_objectfunctie[0][1] == 'Oorspronkelijke functie':
            oorspr_functie = res_objectfunctie[0][0]
        else:
            oorspr_functie = ''

        #The object function could indicate an acheological object, type_obj indicates this and should be filled
        if oorspr_functie == 'Archeologie':
            type_obj = 'A'
        else:
            type_obj = 'G'

        #The cbs_tekst is a further description of the object function in main categories.
        if res_object[0][4] is not None:
            cbs_tekst = res_object[0][4]
        else:
            cbs_tekst = ''
        if type_obj == 'A':
            cbs_tekst = ''

        #Sometimes there are build years. Indicated by a start and an end year (if these are the same only start is shown)
        if not res_objectbouwactiviteit == []:
            if res_objectbouwactiviteit[0][7] == 'Oorspronkelijk bouwjaar':
                bouwjaar = str(res_objectbouwactiviteit[0][2])
                if not bouwjaar == str(res_objectbouwactiviteit[0][3]):
                    bouwjaar = bouwjaar + '-' + str(res_objectbouwactiviteit[0][3])
            else:
                bouwjaar = ''
        else:
            bouwjaar = ''

        #On few occassions the architect (or builder) is indicated within the database.
        if not res_objectambacht == []:
            if not res_objectambacht[0][7] is None and not res_objectambacht[0][6] is None:
                architect = res_objectambacht[0][7] + ' ' + res_objectambacht[0][6]
            if not res_objectambacht[0][6] is None:
                architect = res_objectambacht[0][6]
            else:
                architect = ''
        else:
            architect=''

        #The lat an lon are in Rijksdriehoekscoordinaten and get converted to international wgs84 standard.
        if res_object[0][2] is not None and res_object[0][3] is not None:
            lat, lon = RD_to_WGS84.convert_rd_wgs84(res_object[0][2], res_object[0][3])
            lat = str(lat)
            lon = str(lon)
        else:
            lat=''
            lon=''

        #the monument id
        objrijksnr = str(rm_id)

        monumentinformation = {'woonplaats': woonplaats, 'objectnaam': objectnaam, 'type_obj': type_obj,
                               'oorspr_functie': oorspr_functie, 'cbs_tekst': cbs_tekst, 'bouwjaar': bouwjaar,
                               'architect': architect, 'lat': lat, 'lon': lon, 'objrijksnr': objrijksnr,
                               'image': '', 'commonscat': ''}
        return monumentinformation


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
