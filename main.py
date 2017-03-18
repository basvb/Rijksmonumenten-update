import read_database

'''
rce_db = read_database.RCEMonumentsDatabase()
rce_db.all_monuments()
rce_db.close()
'''

wiki_db = read_database.WikipediaMonumentsDatabase()
wiki_db.load_monuments_from_web()
wiki_db.save_monuments_to_file()
