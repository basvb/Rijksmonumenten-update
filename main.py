import read_database

'''
rce_db = read_database.RCEMonumentsDatabase()
rce_db.all_monuments()
rce_db.close()
'''

wiki_db = read_database.WikipediaMonumentsDatabase()
wiki_db.all_monuments()
