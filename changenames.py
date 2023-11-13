#discord changed how usernames work leading to some completely off usernames in the database. this should help i think.

import discord, discord.utils, os, sqlite3, re, traceback

token = "" #discord api client token

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #directs to exact file
db_path = os.path.join(BASE_DIR, "imagestore.db") #database name configured here
conn = sqlite3.connect(db_path, isolation_level=None) #set to apply changes on execution
c = conn.cursor()


intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = discord.Client(intents=intents) #client object

@client.event
async def on_ready():    
    cursor = c.execute("SELECT uid, username FROM images")
    for row in cursor.fetchall():
        user = client.get_user(row[0])
        if user == None:
            print("Cannot Set: " + str(row[1]) + " | New Name: Not Found!")
            continue
        else:
            onlyAlpha = re.compile('[^a-zA-Z]')
            newName = onlyAlpha.sub('', str(user.name).lower())
            c.execute('UPDATE images SET username = ? WHERE uid = ? ', (newName, row[0]))
            print('Setting "' + str(row[1]) + '" to "' + newName + '.')
            continue
    
    exit() #this is messy

client.run(token)