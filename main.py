import read_database
from operator import itemgetter

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
    return '<!---->\n' \
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


def missing_monuments_dump():
    rce_db = read_database.RCEMonumentsDatabase()
    lines = []
    for monument_identifier in missing_monuments_on_wikipedia():
        monument_info = rce_db.get_rce_information_on_monument(monument_identifier)
        rowtemplate = monument_info_to_rowtemplate(monument_info)
        lines.append(('add', monument_info['woonplaats'], monument_info['woonplaats'].lower(), rowtemplate)) #add a tuple with the place and the rowtemplate
    rce_db.close()
    wiki_db = read_database.WikipediaMonumentsDatabase(from_file=True)
    for monument_info in wiki_db.get_monuments_info(no_longer_monument_on_wikipedia()):
        lines.append(('remove', monument_info['municipality'], monument_info['municipality'].lower(), monument_info['id']))
    lines = sorted(lines, key=itemgetter(2)) #sort the rowtemplates based on the place

    text_for_wikipage = ''
    last_location = ''
    adding = False
    deleting = False
    for line in lines:
        if line[2] != last_location:
            last_location = line[2]
            if adding:
                adding = False
                text_for_wikipage += '\n|}'
            if deleting:
                deleting = False
            text_for_wikipage += '\n\n==[[Lijst van rijksmonumenten in {place}]]=='.format(place=line[1])
            if line[0] == 'add':
                adding = True
                text_for_wikipage += '\nMonumenten om toe te voegen:\n{{Tabelkop rijksmonumenten}}'
            else:
                deleting = True
                text_for_wikipage += '\nDe volgende monumenten zijn niet langer een monument:'
        elif adding and not deleting and line[0] == 'remove':
            adding = False
            deleting = True
            text_for_wikipage += '\n|}\n\nDe volgende monumenten zijn niet langer een monument:'
        text_for_wikipage += '\n' + line[3]

    with open("data\monumenten_voor_Wikipedia.txt", "w") as text_file:
        text_file.write(text_for_wikipage)

'''
wiki_db = read_database.WikipediaMonumentsDatabase(from_file=False)
wiki_db.load_monuments_from_web()
wiki_db.save_monuments_to_file()
'''

missing_monuments_dump()
