#Merge 2 fanfiction database files together. Creates a totally new file as to leave the old ones untouched.

import sqlite3

pathA = str(input("Filename for DB A:"))
pathB = str(input("Filename for DB B:"))
pathC = str(input("Output file name:"))

dbA = sqlite3.connect(pathA)
dbB = sqlite3.connect(pathB)
dbC = sqlite3.connect(pathC)

dbC.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='fanfiction' ''')


setupCommand = ('''
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
dbC.execute(setupCommand)

aCursor = dbA.cursor()
aCursor.execute('SELECT * FROM fanfiction')
aOutput = aCursor.fetchall()

for entry in aOutput:
    print("Populating SID:"+str(entry[0]))
    dbC.execute('''INSERT INTO fanfiction (id, canon_type, canon, authorid, title, updated, published, language, genre, rating, chapters, words, reviews, favs, follows, status, story)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', entry)                       
dbC.commit()

del(aOutput)

bCursor = dbB.cursor()
bCursor.execute('SELECT * FROM fanfiction')
bOutput = bCursor.fetchall()

cCursor = dbC.cursor()
for entry in bOutput:
    checkExist = cCursor.execute('''SELECT id FROM fanfiction WHERE id=?''',(int(entry[0]),))
    result = checkExist.fetchone()
    if result:
        print("Already exists, skip SID: "+str(entry[0]))

    else:
        print("Populating SID:"+str(entry[0]))
        dbC.execute('''INSERT INTO fanfiction (id, canon_type, canon, authorid, title, updated, published, language, genre, rating, chapters, words, reviews, favs, follows, status, story)
                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', entry)   
dbC.commit()