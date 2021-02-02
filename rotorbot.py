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
import os, re, discord, discord.utils, sqlite3, os.path, requests, json, asyncio, random
from discord import user
from time import time, ctime

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

#bot tokens
token = config["discord_token"] #discord api client token
clientID=config["imgur_token"] #imgur api client ID

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents) #client object

#project version number printed on documentation
versionNum = "0.9.10"

roleList = ["SA", "FB", "FC", "FD", "RX-8", "MX-5", "gamer"] #list of roles available to assign via bot
locationList =["Northeast", "Southeast", "Midwest", "Southwest", "Northwest", "Europe", "Australia/New Zealand", "Canada"]

#cute catchprases rotorbot will parrot. can be as many or little as you want.
phrases = ["Hello, how are you? (⌒o⌒)", "How can i help you today? (≧◡≦)", "whats up? （＾⊆＾）", "tell me a joke! ^o^", "Hope you're having a fantastic day! ヽ( ´ ∇ ｀ )ノ", "You're doing quite well for yourself"]
phrases2 = ["Why do you even check these? it's like you enjoy getting insulted you perv!", "Sorry can't talk, I wouldn't want you to be late to your recall appointment!", "Don't you have a corvette to be lusting after or something?", "Roses are red, violets are blue, my car is faster and lighter too", "Sorry, but I think your engine is in another castle!", "I've never met a valve I've liked. You're not really changing my mind on that."]
phrases3 = ["Apologies, the ticket window is over there." , "Sorry, I’m not authorised to speak with passengers.", "If you have a question or complaint, please take it up with the transit authority.", "Please be prepared to pay your fare!"]
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
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(activity=discord.Game(name=config['playing_message']))

#welcomes users, mentions them to grab attention, and points them to the welcome channel
@client.event

    ###############################
    ##      Member Join          ##
    ###############################
async def on_member_join(member):

    if member.guild.id == config['server_id']: #checks to see if user is joining r/rx7 discord. this allows for one image db to run on multiple servers.
        await client.wait_until_ready()
        channel = client.get_channel(config['welcome_channel'])
        await channel.send('Hello '+ member.mention +', ' + config['welcome_message'])


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
    
    uid = (message.author.id,) #grabs Discord UID from message author

    if message.author == client.user: # prevents recursive loop
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
        if message.author.id != 701871518530928701: #bodge code that literally just bans Rotorican from using the role picker
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
                        if (text[1].capitalize() + " " + text[2].capitalize()) == "New Zealand" or text[1].capitalize() == "Nz":
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
        
        desc = message.content[8:] #gets image description
        match = re.search(r'\bimgur.com\b',desc)
        match1 = re.search(r'\bcdn.discordapp.com\b',desc)
        if match or match1:
            await message.channel.send("~no imgur/discord links allowed in descriptions! include an image with the post and it will be automatically added!")
            return
        if desc == "": #handles error and informs user
            if message.attachments == []:
                await message.channel.send("~uh oh! i've encountered a syntax error! (¤﹏¤)\nremember, "+message.author.name+", the command goes '+addcar ``your text here``'. A description ***MUST*** be included if run for the first time! If you just want to change the image you have saved, attach a new one and run the command again! W^W")
                return #ends add image command to prevent exceptions from occuring due to bad data
            else:
                response = requests.post('https://api.imgur.com/3/upload', data={'image':message.attachments[0].url, 'type':'url'}, headers={'Authorization': ('Client-ID ' + clientID)}) #uploads attachment URL to imgur
                if str(response) == "<Response [200]>": #checks if upload succeeded
                    jsonData = response.json() #reads json data from response

                    c.execute('SELECT * FROM images WHERE UID =?', uid) #pulls user information
                    currentData = (c.fetchone())
                    if currentData == None: #checks to see if user exists in the database
                        await message.channel.send("hmm, i can't seem to find a record on you. i can make one, but to do that i need a description. attach one and i'll see what i can do. v( ‘.’ )v") #sends error message
                        return
                    else:
                        c.execute('UPDATE images SET link = ? WHERE uid = ? ', (jsonData['data']['link'], message.author.id)) #updates existing information
                        await message.channel.send("~~thank you!!! ^>^\nyour data has been updated! have a nice day! {◕ ◡ ◕}") #sends confirmation
                        return
                elif str(response) == "<Response [417]>": #checks if 417, which is probably too large for the API to handle
                    await message.channel.send("Error! Imgur Upload Failed! HTTP Status Code 417: Bad Header! This is probably happening because the image you are uploading is too large to be processed by the API. Make sure your image is smaller than 10mb and try again! ") #sends confirmation
                    return
                else: #if upload isn't successful, throws an error
                    await message.channel.send("Error! Imgur Upload Failed! Either Imgur is down or there is a problem with your image.\nfor debugging: http " + str(response)) #sends confirmation
                    return
        
        if message.attachments == []: #checks to make sure that user has included an attachment, and updates their record without an image
            c.execute('SELECT * FROM images WHERE UID =?', uid) #pulls user information
            currentData = (c.fetchone())
            if currentData == None: #checks to see if user exists in the database
                await message.channel.send("hmm, i can't seem to find a record on you. i can make one, but to do that i need an image. attach one and i'll see what i can do. v( ‘.’ )v") #sends error message
            else:
                c.execute('UPDATE images SET description = ? WHERE uid = ? ', (desc, message.author.id)) #updates existing information
                await message.channel.send("~~thank you!!! ^>^\nyour data has been updated! have a nice day! {◕ ◡ ◕}") #sends confirmation
            return #ends add image command to prevent exceptions from occuring due to bad data


        response = requests.post('https://api.imgur.com/3/upload', data={'image':message.attachments[0].url, 'type':'url'}, headers={'Authorization': ('Client-ID ' + clientID)}) #uploads attachment URL to imgur
        if str(response) == "<Response [200]>": #checks if upload succeeded
            jsonData = response.json() #reads json data from response

            c.execute('SELECT * FROM images WHERE UID =?', uid) #pulls user information
            currentData = (c.fetchone())
            if currentData == None: #checks to see if user exists in the database
                await message.channel.send("hmm, i can't seem to find a record on you. let me create one real quick... ╰(◡‿◡✿╰)") #sends error message
                c.execute('INSERT INTO images VALUES (?,?,?,?)', (''.join(filter(str.isalnum, message.author.name.lower())), message.author.id, desc, jsonData['data']['link'])) #creates new values using user account and provided information
                await message.channel.send("~~lovely. i created a record and added in your information! have a nice day! (^▽^)") #sends success message
            else:
                c.execute('UPDATE images SET description = ?, link = ? WHERE uid = ? ', (desc, jsonData['data']['link'], message.author.id)) #updates existing information
                await message.channel.send("~~thank you!!! ^>^\nyour data has been updated! have a nice day! {◕ ◡ ◕}") #sends confirmation
        elif str(response) == "<Response [417]>": #checks if 417, which is probably too large for the API to handle
            await message.channel.send("Error! Imgur Upload Failed! HTTP Status Code 417: Bad Header! This is probably happening because the image you are uploading is too large to be processed by the API. Make sure your image is smaller than 10mb and try again! ") #sends confirmation
            return
        else: #if upload isn't successful, throws an error
            await message.channel.send("Error! Imgur Upload Failed! Either Imgur is down or there is a problem with your image.\nfor debugging: http " + str(response)) #sends confirmation
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
            photo.set_image(url=str(message.author.avatar_url))
            photo.set_author(name=titleName, icon_url=message.author.avatar_url)
            photo.set_footer(text=("rotorbot v" + versionNum), icon_url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
            await message.channel.send(embed=photo)
        else: #if a user is mentioned
            titleName = message.mentions[0].name + "'s Avatar:" #grabs username as embed title
            photo = discord.Embed(title=titleName, colour=discord.Colour(0x29aaca)) #created embed
            await message.channel.send("fancy! ＼(^-^)／") #sends success message
            #sets target's avatar, username, and shows what bot handled the command
            photo.set_image(url=str(message.mentions[0].avatar_url))
            photo.set_author(name="request by " + message.author.name, icon_url=message.author.avatar_url)
            photo.set_footer(text=("rotorbot v" + versionNum), icon_url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
            await message.channel.send(embed=photo)

    #lists all users in image database
    elif text[0].lower() == "carlist":
        userString = '**' #string for users
        userString1 = '**' #separate string for usernames over 1000 characters
        c.execute('SELECT Username FROM images') #grabs all usernames from image table
        data = c.fetchall()

        listCounter = 0 #counter for list
        for row in data: #reads all rows
            listCounter = listCounter + 1 #adds one every iteration
            if len(userString) < 1000:
                if listCounter % 6 == 0: #every 5th name add a new line
                    userString = userString + "\n"
                else:
                    userString = (userString + (row[0]) + ", ")
            else:
                if listCounter % 6 == 0: #every 5th name add a new line
                    userString1 = userString1 + "\n"
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
        await message.author.send("Here is a list of all users in the database! Some people might not even be from the same server!")
        await message.author.send(embed=carList)
        if userString1 != "**":
            userString1 = userString1[:-4]
            userString1 = userString1 + "**"
            carList1 = discord.Embed(colour=discord.Colour(0x29aaca)) #creates embed to send car data
            carList1.add_field(name="More Users:", value=userString1)
            carList1.set_footer(text=("rotorbot v" + versionNum), icon_url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
            await message.author.send(embed=carList1)
        return #exits


    #mute for mitsu evo server
   
    if text[0].lower() == 'mute' and message.guild.id == 514951085430013962 and "Admin" in role_names:
        try:
            inputTime = (int(text[2]) * 3600) #converts hour to seconds
            userName = message.mentions[0].id
            serverID = message.guild.id

            t=time()

            newTime = t + float(inputTime)

            data = open(mute_path, "a")

            data.write(str(newTime) + "|"+ str(userName)+"|" + str(serverID) + "|")
            data.close()

            role = discord.utils.get(message.guild.roles, name="Muted") #gets role ID from server
            await message.mentions[0].add_roles(role)
            await message.channel.send("problem user resolution algorithm activated! deploying self reflection period!")
        except:
            await message.channel.send("there has been an internal error. thats all i know.\nsyntax is ``user <time in hours>`` if you forgot. decimal places don't work.")

    #Image Link Handler v0.4 - now ignores case
    firstLetter = message.content[0] #checks if first letter of a message is the invoking one. Can be configured from here.
    if firstLetter == config['invocation_symbol']: #if not invoking, request is thrown out
        
        if message.content.lower()[1:3] == "<@" or message.content.lower()[1:4] == " <@":
            c.execute('SELECT * FROM images WHERE UID =?', [int(message.mentions[0].id)]) #compares pinged UID to DB
            currentData = (c.fetchone())
            if currentData == None: #if no user exists, command ends
                message.channel.send("Sorry! This user does not exist in my memory!")
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
            
#run command
client.run(token)