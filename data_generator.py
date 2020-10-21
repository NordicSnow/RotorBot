################################################################
#     A Quick Script For Adding Test Data To Rotorbot Database #
#                         by Zeke Ross                         #
################################################################

import string, random, sqlite3, os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #directs to exact file
db_path = os.path.join(BASE_DIR, "imagestore.db") #database name configured here
conn = sqlite3.connect(db_path, isolation_level=None) #set to apply changes on execution
c = conn.cursor()

def randString(length):
    letters = string.ascii_lowercase
    finalName = ''.join(random.choice(letters) for i in range(length))
    return finalName

numberEntries = input("How many entries to add: ")

for i in range(int(numberEntries)):
    insertString = randString(6)
    randoID = random.randint(100000000000000000, 999999999999999999)
    randoDescription = randString(20)
    randoLink = "https://i.imgur.com/" + randString(7) + ".jpg/"
    c.execute('INSERT INTO images VALUES (?, ?, ?, ?)', (insertString, randoID, randoDescription, randoLink))
    print('"' + insertString + '" added.')