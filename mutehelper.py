#Framework for rotorbot mute helper
import os, discord, json
from time import time, sleep, strptime

from discord.guild import Guild

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #directs to exact file
file_path = os.path.join(BASE_DIR, "mutedusers.rbot") #dummy file
config_path = os.path.join(BASE_DIR, 'config.json')
with open(config_path, "r") as read_file:
    config = json.load(read_file)
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents) #client object
token = config["discord_token"] #discord api client token

@client.event
async def on_ready():

    await client.wait_until_ready()
    print(f'{client.user.name} has connected to Discord!')
    t=time()
    
 
    while True:
        t=time()
        data = open(file_path, "r")
        inData = data.read()

        if inData == '':
            sleep(10)
            #print("nothing.")
        else:
            muteData = inData.split("|")
            muteData.pop()
            for i in range(0, len(muteData), 3):
                if t > float(muteData[i]):
                    currGuild = client.get_guild(int(muteData[i+2]))
                    role = discord.utils.get(currGuild.roles, name="Muted") #gets role ID from server
                    currUser = currGuild.get_member(int(muteData[i+1]))
                    await currUser.remove_roles(role)
                    data.close()
                    muteData.pop(i)
                    muteData.pop(i)
                    muteData.pop(i)
                    data = open(file_path, "w")
                    newString = ""
                    for z in range(len(muteData)):
                        newString += muteData[z] + "|"
                    data.write(newString)
                    data.close()
                    break
                else:
                    print("User " + muteData[i+1] +" is banned")
            sleep(5)


client.run(token)