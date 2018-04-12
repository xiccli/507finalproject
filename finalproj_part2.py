import json
import sqlite3

DBNAME = 'species.db'
SPECIESJS = 'species_detail.json'
## ----------------------2.1 create a new database called species.db----------------
try:
    print ("connect to local sql file...")
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
except:
    print ("error")

check_spc='''
    DROP TABLE IF EXISTS 'Species';
'''
cur.execute(check_spc)
create_table_spc='''
    CREATE TABLE Species(
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        'Name' TEXT,
        'Status' TEXT,
        'Population' TEXT,
        'ScientificName' TEXT,
        'Height' TEXT,
        'Weight' TEXT,
        'Length' TEXT,
        'Habitats' TEXT,
        'Place' TEXT,
        'GeneralHabitat' TEXT
    )
'''
cur.execute(create_table_spc)
## ----------------------2.2 input data into the db----------------
insert_species='''
    INSERT INTO Species (Name,Status,Population,ScientificName,Height,Weight,Length,Habitats,Place,GeneralHabitat) VALUES (?,?,?,?,?,?,?,?,?,?);
'''
with open(SPECIESJS) as f_species:
    species_ls=[]
    species_dr=json.load(f_species)
    for each in species_dr:
        species_ls.append((each,species_dr[each]['Status'],species_dr[each]['Population'],species_dr[each]['Scientific Name'],species_dr[each]["Height"],species_dr[each]["Weight"],species_dr[each]["Length"],species_dr[each]["Habitats"],species_dr[each]["Place"],species_dr[each]["General Habitat"]))
    # del countries_ls[0]
    for each in species_ls:
        cur.execute(insert_species,each)
conn.commit()
conn.close()
