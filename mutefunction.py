
import discord, os

client = discord.Client() #client object

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #directs to exact file
file_path = os.path.join(BASE_DIR, "mutedusers.rb") #database name configured here

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    
    if message.content == "" or message.content == "+": #ignores messages with only images in them
        return

    #pulls all roles for a given user
    try:
        role_names = [role.name for role in message.author.roles]
    except:
        return

    role_names.pop(0)

    if message.author == client.user: # prevents recursive loop
        return

    if message.content[0] == config['invocation_symbol']:
        commandName = message.content.lower()[1:]
        text = commandName.split()
    else:
        return

#mute for mitsu evo server
    
    if text[0].lower() == 'mute' and message.guild.id == 514951085430013962 and "Admin" in role_names:
        try:
            timeSet = (int(text[2]) * 3600) #converts hour to seconds
            role = discord.utils.get(message.guild.roles, name="Muted") #gets role ID from server
            await message.mentions[0].add_roles(role)
            await message.channel.send("problem user resolution algorithm activated! deploying self reflection period!")

            await asyncio.sleep(timeSet) #wait time for cooldown
            await message.author.remove_roles(role) #removal
            await message.channel.send("punishment of " +message.mentions[0].mention + " revoked!")
        except:
            await message.channel.send("there has been an internal error. thats all i know.\nsyntax is ``user <time in hours>`` if you forgot. decimal places don't work.")