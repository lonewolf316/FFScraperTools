#Import to database from text files downloaded from internetarchive
from urllib.parse import urlparse
from tqdm import tqdm
import sqlite3, os

def textfileparse(fileName):
    
    #Initialize dictionary with None to prevent errors later if any metadata is missing
    paramDict = {"id":None, "canon_type":None, "canon":None, "authorid":None, "title":None, "updated":None, "published":None, "language":None,
     "genre":None, "rating":None, "chapters":None, "words":None, "reviews":None, "favs":None, "follows":None, "status":None, "story":None,}

    storyString = ""

    txtFile = open(fileName, "rt")
    contents = txtFile.read()
    txtFile.close()
    contents = contents.splitlines()

    paramDict["title"] = contents[3]
    
    x = 0
    for line in contents:
        if x < 25:
            if line.startswith("Category:"):
                paramDict["canon"] = line[10:]
            elif line.startswith("Genre:"):
                paramDict["genre"] = line[7:]
            elif line.startswith("Language:"):
                paramDict["language"] = line[10:]
            elif line.startswith("Status:"):
                paramDict["status"] = line[8:]
            elif line.startswith("Published:"):
                paramDict["published"] = line[11:]
            elif line.startswith("Updated:"):
                paramDict["updated"] = line[9:]
            elif line.startswith("Rating:"):
                paramDict["rating"] = line[8:]
            elif line.startswith("Chapters:"):
                paramDict["chapters"] = line[10:]
            elif line.startswith("Words:"):
                paramDict["words"] = line[7:]
            elif line.startswith("Story URL:"):
                paramDict["id"] = int(line[11:].split("/")[4])
            elif line.startswith("Author URL:"):
                paramDict["authorid"] = int(line[12:].split("/")[4])
        else:
            storyString += str(line) + "\n "
        x+=1
    paramDict["story"] = storyString
    return(paramDict)


connection = sqlite3.connect('importFanfiction.db')
c = connection.cursor()

c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='fanfiction' ''')

if c.fetchone()[0]==0:
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
    c.execute(sql_command)
    print("Created Table")
else:
    print("Table exists")

rootdir = "../Downloads"
#rootdir = input("Root Directory:")
allNames =[]

x=0
for root, dirs, files in os.walk(rootdir, topdown = False):
    for name in files:
        x+=1
        allNames.append(os.path.join(root,name))
        print("Files found:", x, end="\r")
        

print("Found", len(allNames), "files.")

print("Sorting.")
allNames.sort()
print("Writing file list")
with open('foundfiles.txt', 'w') as f:
    for item in allNames:
        f.write("%s\n" % item)

print("Importing")
for fileName in tqdm(allNames):
    storyDict = textfileparse(fileName)
    storyID = storyDict.get("id")
    c.execute('SELECT 1 FROM fanfiction WHERE id=? LIMIT 1', (storyID,))
    exists = c.fetchone()    
    if exists == None:       
        c.execute('''INSERT INTO fanfiction (id, canon_type, canon, authorid, title, updated, published, language, genre, rating, chapters, words, reviews, favs, follows, status, story)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (storyDict.get('id'), storyDict.get('canon_type'), storyDict.get('canon'), storyDict.get('authorid'), storyDict.get('title'), storyDict.get('updated'), storyDict.get('published'), storyDict.get('language'), storyDict.get('genre'), storyDict.get('rating'), storyDict.get('chapters'), storyDict.get('words'), storyDict.get('reviews'), storyDict.get('favs'), storyDict.get('follows'), storyDict.get('status'), storyDict.get("story")))
        connection.commit()
    else:
        pass

    