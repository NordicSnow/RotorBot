import os, sqlite3, json
from PIL import Image, ImageOps

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #directs to exact file
db_path = os.path.join(BASE_DIR, "imagestore.db") #database name configured here
file_path = os.path.join(BASE_DIR, "rbot.json") #export file

conn = sqlite3.connect(db_path, isolation_level=None) #set to apply changes on execution
c = conn.cursor()

c.execute("SELECT Username, Link FROM IMAGES")
data = c.fetchall()

userNum = len(data)

for i in range(userNum):
    print("User " + str(i) + " of " + str(userNum) + " || Current User: " + data[i][0])

    imgFile = (data[i][1]).split("/")[-1]
    fType = imgFile.lower().split(".")[-1]


    fType = BASE_DIR + "/rbot/" + imgFile
    fURL = "i.rotorhead.club/min/" + imgFile +".jpg"

    try:
        picture = Image.open(fType)
    except:
        continue
    picture = ImageOps.exif_transpose(picture)
    rgb_picture = picture.convert('RGB')
    rgb_picture.save(BASE_DIR +"/min/" +imgFile + ".jpg", 
                 "JPEG", 
                 optimize = True, 
                 quality = 40)
    
    c.execute('UPDATE images SET minImg = ? WHERE username = ? ', (fURL, data[i][0])) #updates existing information
    
c.execute('SELECT * FROM images')
data = c.fetchall()
finalDict = {}
for i in range(len(data)):
        finalDict[data[i][0]] = {'UID': data[i][1], 'Desc' : data[i][2], "Link": data[i][3], "GID" : data[i][4], "minLink" : data[i][5]}

with open(file_path, 'w') as jsonFile:
    json.dump(finalDict, jsonFile, indent=4, sort_keys=True)