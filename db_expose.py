import os, sqlite3, json, time

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #directs to exact file
db_path = os.path.join(BASE_DIR, "imagestore.db") #database name configured here
conn = sqlite3.connect(db_path, isolation_level=None) #set to apply changes on execution
file_path = os.path.join(BASE_DIR, "rbot.json") #export file
c = conn.cursor()


while True:
    c.execute('SELECT * FROM images')
    data = c.fetchall()

    #print(type(data))
    finalDict = {}
    for i in range(len(data)):
        finalDict[data[i][0]] = {'UID': data[i][1], 'Desc' : data[i][2], "Link": data[i][3]}

    with open(file_path, 'w') as jsonFile:
        json.dump(finalDict, jsonFile, indent=4, sort_keys=True)

    time.sleep(3600)