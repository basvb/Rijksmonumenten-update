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

def missing_monuments_wikitemplates():
    rce_db = read_database.RCEMonumentsDatabase()
    rce_db.understand_database()
    rce_db.monument_as_rowtemplate(14453)
    rce_db.monument_as_rowtemplate(514045)
    rce_db.monument_as_rowtemplate(530912)
    rce_db.monument_as_rowtemplate(516836)
    rce_db.close()

missing_monuments_wikitemplates()
#print(len(no_longer_monument_on_wikipedia()))
#print(len(missing_monuments_on_wikipedia()))