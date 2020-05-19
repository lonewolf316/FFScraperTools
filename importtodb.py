#Import to database from text files downloaded from internetarchive
from urllib.parse import urlparse

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
    paramDict["authorid"] = contents[5][3:]
    
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
    print(paramDict)

textfileparse(input("fileName: "))
