import read_database

'''
rce_db = read_database.RCEMonumentsDatabase()
rce_db.all_monuments()
rce_db.close()
'''


def missing_monuments_on_wikipedia():
    wiki_db = read_database.WikipediaMonumentsDatabase(from_file=True)
    wiki_id = wiki_db.all_monuments()
    rce_db = read_database.RCEMonumentsDatabase()
    rce_id = rce_db.all_monuments()
    missing_monuments = list(set(rce_id) - set(wiki_id))

    rce_db.close()
    return missing_monuments

def no_longer_monument_on_wikipedia():
    wiki_db = read_database.WikipediaMonumentsDatabase(from_file=True)
    wiki_id = wiki_db.all_monuments()
    rce_db = read_database.RCEMonumentsDatabase()
    rce_id = rce_db.all_monuments()
    missing_monuments = list(set(wiki_id) - set(rce_id))

    rce_db.close()
    return missing_monuments

def monument_info_to_rowtemplate(monument_info):
    return '\n<!---->\n' \
           '{{{{Tabelrij rijksmonument' \
           '|woonplaats={woonplaats}' \
           '|objectnaam={objectnaam}' \
           '|type_obj={type_obj}' \
           '|oorspr_functie={oorspr_functie}' \
           '|cbs_tekst={cbs_tekst}' \
           '|bouwjaar={bouwjaar}' \
           '|architect={architect}' \
           '|adres={adres}' \
           '|lat={lat}' \
           '|lon={lon}' \
           '|objrijksnr={objrijksnr}' \
           '|image={image}' \
           '|commonscat={commonscat}' \
           '}}}}'\
        .format(woonplaats=monument_info['woonplaats'],
                objectnaam=monument_info['objectnaam'],
                type_obj=monument_info['type_obj'],
                oorspr_functie=monument_info['oorspr_functie'],
                cbs_tekst=monument_info['cbs_tekst'],
                bouwjaar=monument_info['bouwjaar'],
                architect=monument_info['architect'],
                adres=monument_info['adres'],
                lat=monument_info['lat'],
                lon=monument_info['lon'],
                objrijksnr=monument_info['objrijksnr'],
                image=monument_info['image'],
                commonscat=monument_info['commonscat'])

def missing_monuments_wikitemplates():
    rce_db = read_database.RCEMonumentsDatabase()
    rce_db.understand_database()
    rce_db.get_rce_information_on_monument(532483)
    print(monument_info_to_rowtemplate(rce_db.get_rce_information_on_monument(532495)))
    rce_db.get_rce_information_on_monument(531046)
    rce_db.get_rce_information_on_monument(531005)
    rce_db.close()


#rce_db = read_database.RCEMonumentsDatabase()
#for id in missing_monuments_on_wikipedia():
#    rce_db.get_rce_information_on_monument(id)
missing_monuments_wikitemplates()
#print(len(no_longer_monument_on_wikipedia()))
#print(len(missing_monuments_on_wikipedia()))