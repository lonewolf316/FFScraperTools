#Finds the lowest and highest SID in a .db file and searches for any missing SIDs in that range.

import sqlite3

pathDb = str(input("Filename for DB:"))

checkDB = sqlite3.connect(pathDb)

dbCursor = checkDB.cursor()
dbCursor.execute('SELECT * FROM fanfiction')
dbOutput = dbCursor.fetchall()

dbSIDS = []
missingSIDS = []

for entry in dbOutput:
    dbSIDS.append(entry[0])

dbMin = min(dbSIDS)
dbMax = max(dbSIDS)


for x in range(dbMin, dbMax):
    print(x)
    checkExist = dbCursor.execute('''SELECT id FROM fanfiction WHERE id=?''',(x,))
    result = checkExist.fetchone()
    if not result:
        missingSIDS.append(x)

print(missingSIDS)
