import os, sqlite3, shutil, requests, random, string

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #directs to exact file
db_path = os.path.join(BASE_DIR, "imagestore.db") #database name configured here

conn = sqlite3.connect(db_path, isolation_level=None) #set to apply changes on execution
c = conn.cursor()

c.execute("SELECT Username, Link FROM IMAGES")
data = c.fetchall()

userNum = len(data)

for i in range(userNum):
    print("User " + str(i) + " of " + str(userNum) + " || Current User: " + data[i][0])

    imgFile = (data[1][1]).split("/")[-1]
    fType = imgFile.lower().split(".")[-1]

    randoString = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6)) #creates a random 6 digit string

    fType = data[i][0] +"_" + randoString + "." + fType
    fURL = "i.rotorhead.club/rbot/" + fType
    #print(fURL)
    #print(fType)
    try:
        response = requests.get(data[i][1], stream = True)
    except:
        continue
    if str(response) == "<Response [200]>": #checks if upload succeeded
        response.raw.decode_content = True

        with open((BASE_DIR +"/rbot/" + fType),'wb') as f:
            shutil.copyfileobj(response.raw, f)
        c.execute('UPDATE images SET link = ? WHERE username = ? ', (fURL, data[i][0])) #updates existing information