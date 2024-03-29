#)>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#)>>>>>>>>>>>>>>>>>>/           \\\>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#)>>>>>>>>>>>>>>>)>>>         \\\+=>..   \\>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#)>>>>>>>>>>>>>> )> (>>>>> )>>          \+=.   \\>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#)>>>>>>>>>>>>>> > )>>>>>>>\>>>               \+<.  \\>>>>>>>>>>>>>>>>>>>>>>>>>>>
#)>>>>>>>>>>>>> )   \>>>>      .)>=\\)))))((((\=>.  +=.  \\>>>>>>>>>>>>>>>>>>>>>>
#)>>>>>>>>>>>>>.> )>>>     .>=\)>>\\)>>>>>>>>((\>>((=(  \<.  \\>>>>>>>>>>>>>>>>>>
#)>>>>>>>>>>>> )   \>\  .)\)>>)>>\\            \\>>/\>/\>   \<.  \>>>>>>>>>>>>>>>
#)>>>>>>>>>>>> (      .>\)>)>>     .)>)>)>).> .    \\>/>>\>     \=  \\>>>>>>>>>>>
#)>>>>>>>>>>>> >     )\)>)>\   ).)>>>=\\\\\\<>>>>)    \>/>(\>      \=  \>>>>>>>>>         _           _          _            _            _           _               _          _       
#)>>>>>>>>>>>>.>   ./)>\>>  ..)>>\))>>>>>>>>>>>(\>>>.   \>\>\>        \> /\>>>>>>        /\ \        /\ \       /\ \         /\ \         /\ \        / /\            /\ \       /\ \     
#)>>>>>>>>>>>>+>  ./)>)>   )>>>\)>>>>>>>>>>>>>>>>>/\>>   )>)>/>  )>>>   /)  \>>>>       /  \ \      /  \ \      \_\ \       /  \ \       /  \ \      / /  \          /  \ \      \_\ \    
#)>>>>>>>>>>>>+>  )\>)>   (\>\)>\\\\\\\\\\\\\\\\\\\>\>>   )>)>)>  \=\.)>. +> />>>      / /\ \ \    / /\ \ \     /\__ \     / /\ \ \     / /\ \ \    / / /\ \        / /\ \ \     /\__ \   
#)>>>>>>>>>>>>+> )>)>)>  .)>>)>>                  )>>)>>.  )>)>>   )>>>>>> )>>>>>     / / /\ \_\  / / /\ \ \   / /_ \ \   / / /\ \ \   / / /\ \_\  / / /\ \ \      / / /\ \ \   / /_ \ \  
#)>>>>>>>>>>>> > )>\)>  .)>>)>>>>>>>>>>>>>>>     .>>>+\>>  )>)>)   />>>>>>  >\)>>    / / /_/ / / / / /  \ \_\ / / /\ \ \ / / /  \ \_\ / / /_/ / / / / /\ \_\ \    / / /  \ \_\ / / /\ \ \ 
#)>>>>>>>>>>>> ( )>>)>  +)>>)>>>>>>>>>>>>>\    .)>>>>>)>=  )>)>)>  ..(\\  .> )>>>   / / /__\/ / / / /   / / // / /  \/_// / /   / / // / /__\/ / / / /\ \ \___\  / / /   / / // / /  \/_/ 
#)>>>>>>>>>>>> ) )>\>>  +\>>)>>>>>>>>>>>\    .)>>>>>>)>>\  )>)>)  +>>>>  )\ )>>>>  / / /_____/ / / /   / / // / /      / / /   / / // / /_____/ / / /  \ \ \__/ / / /   / / // / /        
#)>>>>>>>>>>>> )>+>)>)>   )>>)>>>>>>>>\    .(>>>>>>>>)>>   )>)>>        / .)>>>>> / / /\ \ \  / / /___/ / // / /      / / /___/ / // / /\ \ \  / / /____\_\ \  / / /___/ / // / /         
#)>>>>>>>>>>>>> > )>\/>   ))>>\>>>>>>    .(>>>>>>>>\)>>   )>)>)>      /\ )>>>>>>>/ / /  \ \ \/ / /____\/ //_/ /      / / /____\/ // / /  \ \ \/ / /__________\/ / /____\/ //_/ /          
#)>>>>>>>>>>>>> )  \/>/>   +=>> \>(.....)>>>>>>>>\)>>=   )>)>)>     /\ )>>>>>>>>>\/_/    \_\/\/_________/ \_\/       \/_________/ \/_/    \_\/\/_____________/\/_________/ \_\/           
#)>>>>>>>>>>>>> +>  \/>/\>   \)>>(/\>>>>>>>>>>\.)>>>   .)>)>)>    /\ )>>>>>>>>>>>
#)>>>>>>>>>>>>>> \   \>\>/>>   /\)>>>>>>))>>>>>>>\   .)>)>\/   .+ .)>>>>>>>>>>>>>                          ~ a project by nordic for the r/rx7 community ~
#)>>>>>>>>>>>>>> +>    \(\>/\>.      \/>\>\ \      )>>)>\)\  /\ .)>>>>>>>>>>>>>>>
#)>>>>>>>>>>>>>>> )      \>/\>(\>>..         ..)>>\)>>\>\ )< .)>>>>>>>>>>>>>>>>>>
#)>>>>>>>>>>>>>>>> \        \=(\>>>((\\>>>>\\\))>>\)=\ .<  )>>>>>>>>>>>>>>>>>>>>>
#)>>>>>>>>>>>>>>>>  >  ))>>     \\==((((\\\\))>=\\  )<\ )>>>>>>>>>>>>>>>>>>>>>>>>
#)>>>>>>>>>>>>>>>>> +>  \>>...                   /<  )>>>>>>>>>>>>>>>>>>>>>>>>>>>
#)>>>>>>>>>>>>>>>>>> +>  )>>>>>>.)>>>        .>\ .)>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#)>>>>>>>>>>>>>>>>>>>  > />>>>>> /<>     .>\ .))>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#)>>>>>>>>>>>>>>>>>>>>> \  \\\\     .><\ .))>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#)>>>>>>>>>>>>>>>>>>>>>>)>>>>>>=+\  .))>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#)>>>>>>>>>>>>>>>>>>>>>>>>(\.)>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#)>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# libraries
import os, re, discord, discord.utils, sqlite3, os.path, requests, json, random, magic, traceback, asyncio, string
from time import time
from PIL import Image, ImageOps

#io
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #directs to exact file
db_path = os.path.join(BASE_DIR, "imagestore.db") #database name configured here
config_path = os.path.join(BASE_DIR, 'config.json')
mute_path = os.path.join(BASE_DIR, "mutedusers.rbot") #mute file
conn = sqlite3.connect(db_path, isolation_level=None) #set to apply changes on execution
c = conn.cursor()

#grabs config data
with open(config_path, "r") as read_file:
    config = json.load(read_file)

#api export file
file_path = os.path.join(BASE_DIR, "rbot.json") #export file
#bot tokens
token = config["discord_token"] #discord api client token
clientID=config["imgur_token"] #imgur api client ID

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
client = discord.Client(intents=intents) #client object

#banned users
timeList = []

#project version number printed on documentation
versionNum = "0.9.11"

carEmojiMessageID = 1173433306184962059
locationEmojiMessageID = 1173433779734462524
interestEmojiMessageID = 1173435004798369833

roleList = ["SA", "FB", "FC", "FD", "RX-8", "MX-5", "gamer"] #list of roles available to assign via bot
locationList =["Northeast", "Southeast", "Midwest", "Southwest", "Northwest", "Europe", "Australia/New Zealand", "Canada"]

#cute catchprases rotorbot will parrot. can be as many or little as you want.
phrases = ["Hello, how are you? (⌒o⌒)", "How can i help you today? (≧◡≦)", "whats up? （＾⊆＾）", "tell me a joke! ^o^", "Hope you're having a fantastic day! ヽ( ´ ∇ ｀ )ノ", "You're doing quite well for yourself"]
phrases2 = ["how goes the swap? not done yet? figures.", "in over your head? you can stop whenever you want <3", "i'll be happy to assist in the process of inserting a Mazda RE into any car. thank you for your consideration!", "its... so... heavy...", "i would be scared if i was your firewall...", "wasn't this supposed to be 'easy'? :wink:", "Why do you even check these? it's like you enjoy getting insulted you perv!", "Sorry can't talk, I wouldn't want you to be late to your recall appointment!", "Don't you have a corvette to be lusting after or something?", "Roses are red, violets are blue, my car is faster and lighter too", "Sorry, but I think your engine is in another castle!", "I've never met a valve I've liked. You're not really changing my mind on that."]
phrases3 = ["Apologies, the ticket window is over there." , "Sorry, I’m not authorized to speak with passengers.", "If you have a question or complaint, please take it up with the transit authority.", "Please be prepared to pay your fare!"]
rallyImages =["https://i.imgur.com/EWeIQuS.jpg"]

#help document
embed = discord.Embed(title="RotorBot Help", colour=discord.Colour(0x29aaca), description=("this is the help document for RotorBot version " + versionNum))
embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
embed.set_author(name="RotorBot", url="https://github.com/NordicSnow/RotorBot", icon_url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
embed.set_footer(text=("rotorbot " + versionNum), icon_url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
embed.add_field(name="Role Picker", value="To add a new role, use the '+addrole' command followed by one of these options:\n***SA***\n***FB***\n***FC***\n***FD***\n***RX-8***\n***MX-5***\n***GAMER***\n There also are location based roles:\n***Northeast***\n***Southeast***\n***Midwest***\n***Northwest***\n***Southwest***\n***Canada***\n***Europe***\n***Australia***\n***New Zealand (or just NZ)***")
embed.add_field(name="Show an image of a user's car", value="To see a given user's car, just type in a '+' followed by their username, eg '+nordic'.")
embed.add_field(name="Add or edit image linker data", value="To add or edit a user image saved in the image linker, use the command '+addcar ``your description here``' and attach your image to the message. This command can also be used to edit an existing dataset. To just change the description you do not need to attach an image. Similarly, to change the image you don't have to include a description.")
embed.add_field(name="View user list", value="To see a list of viewable cars people have saved, type ``+carlist`` and a full list will be DMed to you!")

#for public servers not using role picker
embedNo7 = discord.Embed(title="RotorBot Help", colour=discord.Colour(0x29aaca), description=("this is the help document for RotorBot version " + versionNum))
embedNo7.set_thumbnail(url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
embedNo7.set_author(name="RotorBot", url="https://github.com/NordicSnow/RotorBot", icon_url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
embedNo7.set_footer(text=("rotorbot " + versionNum), icon_url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
embedNo7.add_field(name="Show an image of a user's car", value="To see a given user's car, just type in a '+' followed by their username, eg '+nordic'.")
embedNo7.add_field(name="Add or edit image linker data", value="To add or edit a user image saved in the image linker, use the command '+addcar ``your description here``' and attach your image to the message. This command can also be used to edit an existing dataset. To just change the description you do not need to attach an image. Similarly, to change the image you don't have to include a description.")
embedNo7.add_field(name="View user list", value="To see a list of viewable cars people have saved, type ``+carlist`` and a full list will be DMed to you!")
#shows console ready message and changes game status

#File downloader
async def writeImage(message, c):
    #grabs last file to delete
    c.execute("SELECT Link, minImg from images where UID = ?", (message.author.id, ))
    currentData = (c.fetchone())
    if currentData != None:
        fileToYeet = currentData[0].split("/")[-1]
        fileToYeet=BASE_DIR +"/rbot/" + fileToYeet
        if os.path.exists(fileToYeet):
            os.remove(fileToYeet)
        else:
            pass
        fileToYeet = currentData[1].split("/")[-1]
        fileToYeet=BASE_DIR +"/min/" + fileToYeet
        if os.path.exists(fileToYeet):
            os.remove(fileToYeet)
        else:
            pass

    imgFile = (message.attachments[0].url).split("/")[-1]
    #removes junk from discord update
    splitFile = imgFile.split("?ex=")
    imgFile=splitFile[0]
    fType = imgFile.lower().split(".")[-1]
    print(fType)
    onlyAlpha = re.compile('[^a-zA-Z]')
    name = onlyAlpha.sub('', message.author.name.lower())
    if name == "":
        name = "unsupportedName"
        #await message.channel.send("Your Discord name needs one or more English alphabetical character or a number in it to use Rotorbot! I can't write a file otherwise! This limitation might get removed in the future but for now I have to ask you to change names. Contact Nordic#5412 for help!")
    randoString = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6)) #creates a random 6 digit string
    fType = name + "_" + randoString + "." + fType
    fURL = "https://i.rotorhead.club/rbot/" + fType

    response = requests.get(message.attachments[0].url, stream = True)
    if str(response) == "<Response [200]>":
        response.raw.decode_content = True
        file = response.raw.read()
        validation = magic.from_buffer(file[:1024])
        validation = validation.split(" ")
        if validation[0] != "JPEG" and validation[0] != "PNG":
            await message.channel.send("Filetype " + validation[0] + " is not supported. Please reupload in JPG or PNG format.")
            return
        currImage = BASE_DIR +"/rbot/" + fType
        with open(currImage,'wb') as f:
            f.write(file)
        return True, fURL, currImage
    else:
        return False, fURL, ""

def updateAPI (currImage, c, UID):

    fileName = currImage.split("/")[-1]

    picture = Image.open(currImage)
    picture = ImageOps.exif_transpose(picture)
    rgb_picture = picture.convert('RGB')
    rgb_picture.save(BASE_DIR +"/min/" +fileName + ".jpg", 
                 "JPEG", 
                 optimize = True, 
                 quality = 40)

    finalLink = "https://i.rotorhead.club/min/" + fileName + ".jpg"
    c.execute('UPDATE images SET minImg = ? WHERE UID = ?', (finalLink, UID))
    c.execute('SELECT * FROM images')
    data = c.fetchall()

    #print(type(data))
    finalDict = {}
    for i in range(len(data)):
            finalDict[data[i][0]] = {'UID': data[i][1], 'Desc' : data[i][2], "Link": data[i][3], "GID" : data[i][4], "minLink" : data[i][5]}

    with open(file_path, 'w') as jsonFile:
        json.dump(finalDict, jsonFile, indent=4, sort_keys=True)
    return True

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(activity=discord.Game(name=config['playing_message']))

    while True:
        t=time()
        global timeList
        if timeList == []:
            await asyncio.sleep(10)
        else:
            for i in range(len(timeList)):
                if t > float(timeList[i][0]):
                    currGuild = client.get_guild(timeList[i][2])
                    role = discord.utils.get(currGuild.roles, name="Muted") #gets role ID from server
                    currUser = currGuild.get_member(timeList[i][1])
                    await currUser.remove_roles(role)
                else:
                    await asyncio.sleep(5)

@client.event
async def on_raw_reaction_add(payload):
    #print(str(payload.emoji))
    async def addRoleFromEmoji(payload, roleName):
        role = discord.utils.get((client.get_guild(payload.guild_id)).roles, name=roleName)
        await payload.member.add_roles(role) #assigns role to user
        await payload.member.send('Role ' + roleName +' Added!')

    #SA
    if str(payload.emoji) == "<:12abest:974087344867115038>" and payload.message_id == carEmojiMessageID:
        await addRoleFromEmoji(payload, "SA")
    #FB
    if str(payload.emoji) == "<:fb:1173418975477121145>" and payload.message_id == carEmojiMessageID:
        await addRoleFromEmoji(payload, "FB")
    #FC
    if str(payload.emoji) == "<:fc:1173418993101582386>" and payload.message_id == carEmojiMessageID:
        await addRoleFromEmoji(payload, "FC")
    #FD
    if str(payload.emoji) == "<:fd:1173419006569500744>" and payload.message_id == carEmojiMessageID:
        await addRoleFromEmoji(payload, "FD")
    #RX-8
    if str(payload.emoji) == "🎱" and payload.message_id == carEmojiMessageID:
        await addRoleFromEmoji(payload, "RX-8")
    #MX-5
    if str(payload.emoji) == "<:mx5:1173419024261054495>" and payload.message_id == carEmojiMessageID:
        await addRoleFromEmoji(payload, "MX-5")


    if str(payload.emoji) == "🌲" and payload.message_id == locationEmojiMessageID:
        await addRoleFromEmoji(payload, "Northeast")
    if str(payload.emoji) == "🌴" and payload.message_id == locationEmojiMessageID:
        await addRoleFromEmoji(payload, "Southeast")
    if str(payload.emoji) == "🌽" and payload.message_id == locationEmojiMessageID:
        await addRoleFromEmoji(payload, "Midwest")
    if str(payload.emoji) == "🏜️" and payload.message_id == locationEmojiMessageID:
        await addRoleFromEmoji(payload, "Southwest")
    if str(payload.emoji) == "🌫️" and payload.message_id == locationEmojiMessageID:
        await addRoleFromEmoji(payload, "Northwest")
    if str(payload.emoji) == "🏰" and payload.message_id == locationEmojiMessageID:
        await addRoleFromEmoji(payload, "Europe")
    if str(payload.emoji) == "🦘" and payload.message_id == locationEmojiMessageID:
        await addRoleFromEmoji(payload, "Australia/New Zealand")
    if str(payload.emoji) == "🍁" and payload.message_id == locationEmojiMessageID:
        await addRoleFromEmoji(payload, "Canada")

    if str(payload.emoji) == "🎮" and payload.message_id == interestEmojiMessageID:
        await addRoleFromEmoji(payload, "gamer")
    if str(payload.emoji) == "🏍️" and payload.message_id == interestEmojiMessageID:
        await addRoleFromEmoji(payload, "🚲💧Bike Chad")

@client.event
async def on_raw_reaction_remove(payload):
    async def removeRoleFromEmoji(payload, roleName):
        role = discord.utils.get((client.get_guild(payload.guild_id)).roles, name=roleName)
        currGuild = client.get_guild(payload.guild_id)
        member = currGuild.get_member(payload.user_id)
        await member.remove_roles(role) #removes role from user
        await member.send('Role ' + roleName +' Removed!')

    #SA
    if str(payload.emoji) == "<:12abest:974087344867115038>" and payload.message_id == carEmojiMessageID:
        await removeRoleFromEmoji(payload, "SA")
    #FB
    if str(payload.emoji) == "<:fb:1173418975477121145>" and payload.message_id == carEmojiMessageID:
        await removeRoleFromEmoji(payload, "FB")
    #FC
    if str(payload.emoji) == "<:fc:1173418993101582386>" and payload.message_id == carEmojiMessageID:
        await removeRoleFromEmoji(payload, "FC")
    #FD
    if str(payload.emoji) == "<:fd:1173419006569500744>" and payload.message_id == carEmojiMessageID:
        await removeRoleFromEmoji(payload, "FD")
    #RX-8
    if str(payload.emoji) == "🎱" and payload.message_id == carEmojiMessageID:
        await removeRoleFromEmoji(payload, "RX-8")
    #MX-5
    if str(payload.emoji) == "<:mx5:1173419024261054495>" and payload.message_id == carEmojiMessageID:
        await removeRoleFromEmoji(payload, "MX-5")

    if str(payload.emoji) == "🌲" and payload.message_id == locationEmojiMessageID:
        await removeRoleFromEmoji(payload, "Northeast")
    if str(payload.emoji) == "🌴" and payload.message_id == locationEmojiMessageID:
        await removeRoleFromEmoji(payload, "Southeast")
    if str(payload.emoji) == "🌽" and payload.message_id == locationEmojiMessageID:
        await removeRoleFromEmoji(payload, "Midwest")
    if str(payload.emoji) == "🏜️" and payload.message_id == locationEmojiMessageID:
        await removeRoleFromEmoji(payload, "Southwest")
    if str(payload.emoji) == "🌫️" and payload.message_id == locationEmojiMessageID:
        await removeRoleFromEmoji(payload, "Northwest")
    if str(payload.emoji) == "🏰" and payload.message_id == locationEmojiMessageID:
        await removeRoleFromEmoji(payload, "Europe")
    if str(payload.emoji) == "🦘" and payload.message_id == locationEmojiMessageID:
        await removeRoleFromEmoji(payload, "Australia/New Zealand")
    if str(payload.emoji) == "🍁" and payload.message_id == locationEmojiMessageID:
        await removeRoleFromEmoji(payload, "Canada")

    if str(payload.emoji) == "🎮" and payload.message_id == interestEmojiMessageID:
        await removeRoleFromEmoji(payload, "gamer")
    if str(payload.emoji) == "🏍️" and payload.message_id == interestEmojiMessageID:
        await removeRoleFromEmoji(payload, "🚲💧Bike Chad")

#welcomes users, mentions them to grab attention, and points them to the welcome channel
@client.event

    ###############################
    ##      Member Join          ##
    ###############################
async def on_member_join(member):

    if member.guild.id == config['server_id']: #checks to see if user is joining r/rx7 discord. this allows for one image db to run on multiple servers.
        await client.wait_until_ready()
        #automatically mutes Santa and hides join message
        if member.id == 527420259976871937:
            role = discord.utils.get(member.guild.roles, name="Muted") #gets role ID from server
            await member.add_roles(role) #assigns role to user
            return
        channel = client.get_channel(config['welcome_channel'])
        await channel.send('Hello '+ member.mention +', ' + config['welcome_message'])


@client.event
async def on_message(message):
    try:

        if message.content == "" or message.content == "+": #ignores messages with only images in them
            return
        
        #pulls all roles for a given user
        try:
            role_names = [role.name for role in message.author.roles]
        except:
            return
        
        #removes @everyone
        role_names.pop(0)
        
        uid = (message.author.id,) #grabs Discord UID from message author

        if message.author == client.user: # prevents recursive loop
            return

        
        if message.channel.id == 820027592349319169:
            return
        ###############################
        ##   NON-SPECIFIC COMMANDS   ##
        ###############################
        #regex for 'built different' statement to inform users of their terrible taste
        match = re.search(r'\bbuilt different\b',message.content.lower())
        match1 = re.search(r"🙈",message.content)

        
        if match or match1 and message.guild.id == config['server_id']: #checks if user has typed in a terribad catchphrase
            emoji = client.get_emoji(800429901076234270)
            await message.add_reaction(emoji)


            
        #sends cute message to user if called on or mentioned.
        if client.user in message.mentions: #checks if user mentions rotorbot
            if "Heretic" in role_names or "I <3 LS" in role_names:

                await message.channel.send(phrases2[random.randint(1, (len(phrases2)-1))])
            elif "Busrider" in role_names:
                await message.channel.send(phrases3[random.randint(1, (len(phrases3)-1))])
            else:
                await message.channel.send(phrases[random.randint(1, (len(phrases)-1))])
        elif message.content.lower() == "rotorbot": # checks if user calls to rotorbot
            if "Heretic" in role_names or "I <3 LS" in role_names:
                await message.channel.send(phrases2[random.randint(1, (len(phrases2)-1))])
            elif "Busrider" in role_names:
                await message.channel.send(phrases3[random.randint(1, (len(phrases3)-1))])
            else:
                await message.channel.send(phrases[random.randint(1, (len(phrases)-1))])

        ###############################
        ##         COMMANDS          ##
        ###############################

        #checks if message invokes the command symbol. If not it stops here.
        if message.content[0] == config['invocation_symbol']:
            commandName = message.content.lower()[1:]
            text = commandName.split()
        else:
            return


        #role assign
        if text[0].lower() == 'addrole' and message.guild.id == config['server_id']: #checks if addcar command is inputed. only works on r/rx7. TODO: move role adding to function to support multiple servers
            if message.author.id != 383924216191254532: #bodge code that literally just bans Rotorican from using the role picker
                if len(text) < 2: #checks if there is a role listed afterwards
                    await message.channel.send("uhhh, you didn't type anything in? tell me what you own and i'll add it! ٩◔‿◔۶") #informs user there was a problem
                    return
                else:
                    if text[1].upper() in role_names:
                        role = discord.utils.get(message.guild.roles, name=text[1].upper()) #id so, it is set and removed.
                        await message.channel.send("awww, sorry to see you go. i've removed the role now. see you around!")
                        await message.author.remove_roles(role)
                        return
                    else:   
                    #todo: make this section less of a bodge
                        if text[1].upper() == "RX8": #checks if command is "rx8", as the actual name of the role is "RX-8"
                            if "RX-8" in role_names:#checks if user already has role
                                role = discord.utils.get(message.guild.roles, name="RX-8") #id so, it is set and removed.
                                await message.channel.send("awww, sorry to see you go. i've removed the role now. see you around!")
                                await message.author.remove_roles(role)
                                return
                            else: #else it is applied
                                role = discord.utils.get(message.guild.roles, name="RX-8") #gets role ID from server
                                await message.author.add_roles(role) #assigns role to user
                                await message.channel.send("~role RX-8 added! welcome! ≧◡≦ <3")
                                return

                        if text[1].upper() == "MX5":#checks if command is "mx5", as the actual name of the role is "RX-8"
                            if "MX-5" in role_names:#checks if user already has role
                                role = discord.utils.get(message.guild.roles, name="MX-5") #id so, it is set and removed.
                                await message.channel.send("awww, sorry to see you go. i've removed the role now. see you around!")
                                await message.author.remove_roles(role)
                                return
                            else: #else it is applied
                                role = discord.utils.get(message.guild.roles, name="MX-5") #gets role ID from server
                                await message.author.add_roles(role) #assigns role to user
                                await message.channel.send("~role MX-5 added! welcome! ≧◡≦ <3")
                                return
                        if text[1].capitalize() == "Australia":
                            role = discord.utils.get(message.guild.roles, name="Australia/New Zealand") #gets role ID from server
                            await message.author.add_roles(role) #assigns role to user
                            await message.channel.send("~'sup person from Australia. I added a role ≧◡≦ <3")
                            return
                        try:
                            if (text[1].capitalize() + " " + text[2].capitalize()) == "New Zealand" or text[1].capitalize() == "NZ":
                                role = discord.utils.get(message.guild.roles, name="Australia/New Zealand") #gets role ID from server
                                await message.author.add_roles(role) #assigns role to user
                                await message.channel.send("~'sup person from New Zealand. I added a role ≧◡≦ <3")
                                return
                        except:
                            pass
                        if text[1].lower() == "gamer":#checks if command is "gamer"
                            if "gamer" in role_names:#checks if user already has role
                                role = discord.utils.get(message.guild.roles, name="gamer") #id so, it is set and removed.
                                await message.channel.send("awww, sorry to see you go. i've removed the role so you won't see any more pings. you can always re-add it if you want back in!")
                                await message.author.remove_roles(role)
                                return
                            else: #else it is applied
                                role = discord.utils.get(message.guild.roles, name="gamer") #gets role ID from server
                                await message.author.add_roles(role) #assigns role to user
                                await message.channel.send("~welcome pro minecrafter! you now are receiving pings for vidya gaming related events! to opt-out, just run the command again. ≧◡≦ <3")
                                return

                        if text[1].lower() == "actually" and text[2].lower() == "runs":
                            if "Actually Runs" in role_names:
                                role = discord.utils.get(message.guild.roles, name="Actually Runs") #id so, it is set and removed.
                                await message.channel.send("awww, that sucks. i've removed the role!")
                                await message.author.remove_roles(role)
                                return
                            else:
                                role = discord.utils.get(message.guild.roles, name="Actually Runs") #gets role ID from server
                                await message.author.add_roles(role) #assigns role to user
                                await message.channel.send("~role Actually Runs added!")
                                return
                        #Assigns roles. Add options to "roleList"
                        if (text[1].upper()) in roleList: #checks input against list "roleList"
                            role = discord.utils.get(message.guild.roles, name=(text[1].upper())) #gets role ID from server
                            await message.author.add_roles(role) #assigns role to user
                            await message.channel.send("~role " +(text[1].upper()) + " added! welcome! ≧◡≦ <3")
                        elif(text[1].capitalize()) in locationList:
                            role = discord.utils.get(message.guild.roles, name=(text[1].capitalize())) #gets role ID from server
                            await message.author.add_roles(role) #assigns role to user
                            await message.channel.send("~'sup person from " +(text[1].capitalize()) + ". I added a role ≧◡≦ <3")
                        else:
                            await message.channel.send("~senpai, i've encountered an error! try assigning a role that exists! (>人<)\n*for a list of available roles, type in '+help'!* (^ｰ^)") #informs user there was a problem
                            return
                                
                            
                            
                    
        if text[0].lower() == 'removerole' and message.guild.id == config['server_id']: #checks if addcar command is inputted. only works on r/rx7. TODO: move role adding to function to support multiple servers
                if message.author.id != 701871518530928701: #bodge code that literally just bans Rotorican from using the role picker
                    if len(text) < 2: #checks if there is a role listed afterwards
                        await message.channel.send("uhhh, you didn't type anything in? tell me what car you want to remove") #informs user there was a problem
                        return
                    else:
                        if text[1].upper() in role_names:
                            role = discord.utils.get(message.guild.roles, name=text[1].upper()) #id so, it is set and removed.
                            await message.channel.send("awww, sorry to see you go. i've removed the role now. see you around!")
                            await message.author.remove_roles(role)
                            return
                        else:
                            await message.channel.send("uhhh, you don't actually own one of those, so i can't remove it.") #informs user there was a problem
                            return
        #add image command
        elif text[0].lower() == 'addcar': #checks to see if command is invoked  
            if message.author.id != 117859345139499008:
                desc = message.content[8:] #gets image description
                try:
                    match = re.search(r'mp4', message.attachments[0].url)
                except:
                    match = False
                match1 = re.search(r'http',desc)
                if match or match1:
                    await message.channel.send("~no imgur/discord links allowed in descriptions! include an image with the post and it will be automatically added!")
                    return
                if desc == "": #handles error and informs user
                    if message.attachments == []:
                        await message.channel.send("~uh oh! i've encountered a syntax error! (¤﹏¤)\nremember, "+message.author.name+", the command goes '+addcar ``your text here``'. A description ***MUST*** be included if run for the first time! If you just want to change the image you have saved, attach a new one and run the command again! W^W")
                        return #ends add image command to prevent exceptions from occuring due to bad data
                    else:
                        c.execute('SELECT * FROM images WHERE UID =?', uid) #pulls user information
                        currentData = (c.fetchone())
                        if currentData == None: #checks to see if user exists in the database
                            await message.channel.send("hmm, i can't seem to find a record on you. i can make one, but to do that i need a description. attach one and i'll see what i can do. v( ‘.’ )v") #sends error message
                            return
                        else:
                            successVar, fURL, currImg = await writeImage(message, c)
                            if successVar== True:
                                c.execute('UPDATE images SET link = ?, GID = ? WHERE uid = ? ', (fURL, message.guild.id, message.author.id)) #updates existing information
                                await message.channel.send("~~thank you!!! ^>^\nyour data has been updated! have a nice day! {◕ ◡ ◕}") #sends confirmation
                                updateAPI(currImg, c, uid[0])
                                return
                            else: #if download isn't successful, throws an error
                                await message.channel.send("Error! There was a problem downloading the image.") #sends confirmation
                                return
                
                if message.attachments == []: #checks to make sure that user has included an attachment, and updates their record without an image
                    c.execute('SELECT * FROM images WHERE UID =?', uid) #pulls user information
                    currentData = (c.fetchone())
                    if currentData == None: #checks to see if user exists in the database
                        await message.channel.send("hmm, i can't seem to find a record on you. i can make one, but to do that i need an image. attach one and i'll see what i can do. v( ‘.’ )v") #sends error message
                    else:
                        c.execute('UPDATE images SET description = ?, GID = ? WHERE uid = ? ', (desc, message.guild.id, message.author.id)) #updates existing information
                        await message.channel.send("~~thank you!!! ^>^\nyour data has been updated! have a nice day! {◕ ◡ ◕}") #sends confirmation
                    return #ends add image command to prevent exceptions from occuring due to bad data


                successVar, fURL, currImg = await writeImage(message, c)
                if successVar== True:

                    c.execute('SELECT * FROM images WHERE UID =?', uid) #pulls user information
                    currentData = (c.fetchone())
                    
                    if currentData == None: #checks to see if user exists in the database
                        await message.channel.send("hmm, i can't seem to find a record on you. let me create one real quick... ╰(◡‿◡✿╰)") #sends error message
                        c.execute('INSERT INTO images VALUES (?,?,?,?,?, ?)', (''.join(filter(str.isalnum, message.author.name.lower())), message.author.id, desc, fURL, message.guild.id, "")) #creates new values using user account and provided information
                        await message.channel.send("~~lovely. i created a record and added in your information! have a nice day! (^▽^)") #sends success message
                        updateAPI(currImg, c, uid[0])
                        
                    else:
                        c.execute('UPDATE images SET description = ?, link = ?, GID = ? WHERE uid = ? ', (desc, fURL, message.guild.id, message.author.id)) #updates existing information
                        await message.channel.send("~~thank you!!! ^>^\nyour data has been updated! have a nice day! {◕ ◡ ◕}") #sends confirmation
                        updateAPI(currImg, c, uid[0])
                    return
                else: #if download isn't successful, throws an error
                    await message.channel.send("Error! There was a problem downloading the image.") #sends confirmation
                    return


        #help command
        elif text[0].lower() == "help": #checks if user typed in help command
            if message.guild.id == config['server_id']:
                await message.channel.send("~this is what you need to say to control me, master (´･ω･`)")
                await message.channel.send(embed=embed) #sends help documentation embed
            else:
                await message.channel.send("~this is what you need to say to control me, master (´･ω･`)")
                await message.channel.send(embed=embedNo7) #sends help documentation embed

        elif text[0].lower() == "iq" and message.guild.id != 551147201619951657: #checks if user has indicated they are dealing with a low IQ individual
                await message.channel.send("To be fair, you have to have a very high IQ to drive an FD RX-7.The car is extremely superior to any other modern supercar, and without a solid grasp of theoretical physics you can't even drive it. There's also it’s linear power delivery, which is deftly woven into it’s driving characterisation- it’s personal philosophy draws heavily from Italian designs, for instance. I personally understand this stuff; I have the intellectual capacity to truly appreciate the supreme handling, to realise that it’s not just good- it says something deep about LIFE. As a consequence people who dislike the FD truly ARE idiots- of course they wouldn't appreciate, for instance, the humour in the FD’s existential catchphrase “Boost in, Apex Seals out,” which itself is a cryptic reference to the tenuous balance between life and death. I'm smirking right now just imagining one of those addlepated simpletons scratching their heads in confusion as Yoichi Sato's genius design unfolds itself on the race track. What fools.. how I pity them. :joy: And yes, by the way, i DO have a FD tattoo. And no, you cannot see it. It's for the ladies' eyes only- and even then they have to demonstrate that they're within 5 IQ points of my own (preferably lower) beforehand. Nothin personnel kid :sunglasses:")
        

        elif text[0].lower() == "avatar": #checks if user wants to see their avatar
            if len(message.mentions) == 0: #checks to see if a user is mentioned, if not it will just show the author's avatar
                titleName = message.author.name + "'s Avatar:" #creates message for embed
                photo = discord.Embed(colour=discord.Colour(0x29aaca)) #creates embed to send avatar in
                await message.channel.send("looking cute! (^L^)") #responds with success message
                #sets avatar image, username, and shows what bot handled the command
                photo.set_image(url=str(message.author.avatar))
                photo.set_author(name=titleName, icon_url=message.author.avatar)
                photo.set_footer(text=("rotorbot v" + versionNum), icon_url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
                await message.channel.send(embed=photo)
            else: #if a user is mentioned
                titleName = message.mentions[0].name + "'s Avatar:" #grabs username as embed title
                photo = discord.Embed(title=titleName, colour=discord.Colour(0x29aaca)) #created embed
                await message.channel.send("fancy! ＼(^-^)／") #sends success message
                #sets target's avatar, username, and shows what bot handled the command
                photo.set_image(url=str(message.mentions[0].avatar))
                photo.set_author(name="request by " + message.author.name, icon_url=message.author.avatar)
                photo.set_footer(text=("rotorbot v" + versionNum), icon_url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
                await message.channel.send(embed=photo)

        #lists all users in image database
        elif text[0].lower() == "carlist":
            userString = '**' #string for users
            userString1 = '**' #separate string for usernames over 1000 characters
            #c.execute('SELECT Username FROM images WHERE GID = ?', (message.guild.id, )) #grabs all usernames from image table
            c.execute('SELECT Username FROM images WHERE GID = 312216330604642305') #grabs all usernames from image table
            data = c.fetchall()

            listCounter = 0 #counter for list
            secondRun = False
            for row in data: #reads all rows
                listCounter = listCounter + 1 #adds one every iteration
                if len(userString) < 1000:
                    if listCounter == 6: #every 5th name add a new line
                        userString = userString +  (row[0]) +  "\n"
                        listCounter = 0
                    else:
                        userString = (userString + (row[0]) + ", ")
                else:
                    if secondRun == False:
                        listCounter = 0
                        secondRun = True
                        userString1 = (userString1 + (row[0]) + ", ")
                        continue
                    if listCounter == 6: #every 5th name add a new line
                        userString1 = userString1 + "\n"
                        listCounter = 0
                    else:
                        userString1 = (userString1 + (row[0]) + ", ")

            userString = userString[:-2]
            userString1 = userString1[:-2]
            userString = userString + "**"
            userString1 = userString1 + "**"
            titleName = "Everybody I Know!" #creates message for embed
            carList = discord.Embed(colour=discord.Colour(0x29aaca)) #creates embed to send car data
            
            await message.channel.send("DMed you!") #responds with success message
            #sets db info, and shows what bot handled the command
            carList.add_field(name="User:", value=userString)
            carList.set_author(name=titleName, icon_url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
            carList.set_footer(text=("rotorbot v" + versionNum), icon_url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
            #await message.channel.send(embed=carList)
            await message.author.send("Here is a list of all users from your server that are in the database!")
            await message.author.send(embed=carList)
            if userString1 != "**":
                userString1 = userString1[:-4]
                userString1 = userString1 + "**"
                carList1 = discord.Embed(colour=discord.Colour(0x29aaca)) #creates embed to send car data
                carList1.add_field(name="More Users: (list went over the character limit!)", value=userString1)
                carList1.set_footer(text=("rotorbot v" + versionNum), icon_url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
                await message.author.send(embed=carList1)
            
            await message.author.send("Bonus: A visual list of all the cars of the RX-7 Discord can be seen here: https://gallery.rotorhead.club/")
            return #exits

        if text[0] == "dbedit" and "Moderators" in role_names:
            if text[1] == "image":
                c.execute('UPDATE images set Link=? where UID =?', (text[3], message.mentions[0].id)) 
                await message.channel.send("Data edited successfully.")
            elif text[1] == "description":
                contentData = " ".join(text[3:])
                c.execute('UPDATE images set Description=? where UID =?', (contentData, message.mentions[0].id)) 
                await message.channel.send("Data edited successfully.")
            if text[1] == "username":
                c.execute('UPDATE images set Username=? where UID =?', (text[3], message.mentions[0].id)) 
                await message.channel.send("Data edited successfully.")

        #mute for mitsu evo server
        if text[0].lower() == 'mute' and message.guild.id == 312216330604642305 and "Moderators" in role_names:
            try:
                global timeList
                inputTime = (int(text[2]) * 3600) #converts hour to seconds
                #inputTime = (int(text[2])) #just runs seconds. only used for testing.
                userName = message.mentions[0].id
                serverID = message.guild.id


                t=time()

                newTime = t + float(inputTime)

                timeList.append([str(newTime), userName, serverID])

                role = discord.utils.get(message.guild.roles, name="Muted") #gets role ID from server
                await message.mentions[0].add_roles(role)
                await message.channel.send("problem user resolution algorithm activated! deploying self reflection period!")
            except:
                await message.channel.send("there has been an internal error. thats all i know.\nsyntax is ``user <time in hours>`` if you forgot. decimal places don't work.")

        #Image Link Handler v0.4 - now ignores case
        firstLetter = message.content[0] #checks if first letter of a message is the invoking one. Can be configured from here.
        if firstLetter == config['invocation_symbol']: #if not invoking, request is thrown out

            #hardcode of nordic in honda server
            if message.guild.id == 867791728177709067:
                if message.content.lower()[1:22] == "<@!52522956294721536>" or message.content.lower()[1:25] == " <@!52522956294721536>" or message.content.lower()[1:] == "nordic":
                    await message.channel.send("Nordic's 2015 Honda CR-Z EX 6MT\nhttps://i.rotorhead.club/rbot/nordic-cr-z.jpg")
                    return

            
            if message.content.lower()[1:3] == "<@" or message.content.lower()[1:4] == " <@":
                c.execute('SELECT * FROM images WHERE UID =?', [int(message.mentions[0].id)]) #compares pinged UID to DB
                currentData = (c.fetchone())
                if currentData == None: #if no user exists, command ends
                    await message.channel.send("Sorry! This user does not exist in my memory!")
                else:
                    await message.channel.send(currentData[2] + "\n" + currentData[3]) #otherwise, information from DB is supplied.
            else:
                commandName = (message.content.lower()[1:],) # checks command name
                c.execute('SELECT * FROM images WHERE Username =?', commandName) #compares command name among populated users
                currentData = (c.fetchone())
                if currentData == None: #if no user exists, command ends
                    return
                else:
                    await message.channel.send(currentData[2] + "\n" + currentData[3]) #otherwise, information from DB is supplied.
    except Exception:
        me = await client.fetch_user(52522956294721536)
        error_message = traceback.format_exc()
        await me.send("***Rotorbot has encountered a problem:***\n`" + error_message +"`")

            
#run command
client.run(token)
