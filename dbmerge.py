#Merge 2 fanfiction database files together. Creates a totally new file as to leave the old ones untouched.

import sqlite3
from tqdm import tqdm

pathA = str(input("Filename for DB A:"))
pathB = str(input("Filename for DB B:"))
pathC = str(input("Output file name:"))

dbA = sqlite3.connect(pathA)
dbB = sqlite3.connect(pathB)
dbC = sqlite3.connect(pathC)
cCursor = dbC.cursor()

cCursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='fanfiction' ''')

if cCursor.fetchone()[0]==0:
    sql_command = ('''
    CREATE TABLE fanfiction (
        id INTEGER PRIMARY KEY,
        canon_type TEXT,
        canon TEXT,
        authorid INTEGER,
        title TEXT,
        updated INTEGER,
        published INTEGER,
        language TEXT,
        genre TEXT,
        rating TEXT,
        chapters INTEGER,
        words INTEGER,
        reviews INTEGER,
        favs INTEGER,
        follows INTEGER,
        status INTEGER,
        story TEXT
    );''')

    cCursor.execute(sql_command)
else:
    print('Table exists')

cCursor = dbC.cursor()
aCursor = dbA.cursor()
aCursor.execute('SELECT * FROM fanfiction')

for entry in aCursor:
    checkExist = cCursor.execute('''SELECT id FROM fanfiction WHERE id=?''',(int(entry[0]),))
    result = checkExist.fetchone()
    if result:
        print("Skipping:", entry[0])
    else:
        dbC.execute('''INSERT INTO fanfiction (id, canon_type, canon, authorid, title, updated, published, language, genre, rating, chapters, words, reviews, favs, follows, status, story)
                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', entry)
        print("Imported: ", entry[0])
        dbC.commit()
bCursor = dbB.cursor()
bCursor.execute('SELECT * FROM fanfiction')


for entry in bCursor:
    checkExist = cCursor.execute('''SELECT id FROM fanfiction WHERE id=?''',(int(entry[0]),))
    result = checkExist.fetchone()
    if result:
        print("Skipping:", entry[0])
    else:
        dbC.execute('''INSERT INTO fanfiction (id, canon_type, canon, authorid, title, updated, published, language, genre, rating, chapters, words, reviews, favs, follows, status, story)
                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', entry)   
        print("Imported: ", entry["id"])
        dbC.commit()