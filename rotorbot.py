# libraries
import os, urllib.request, json, re, discord, discord.utils
from discord.ext import commands



#bot token
token = '<insert token here>' #this should be in a seperate file but its not public so who cares

client = discord.Client() #client object
defaultChannel = client.get_channel(312216330604642305) #sets default channel as #garage

roleList = ["SA", "FB", "FC", "FD", "RX-8", "MX-5"] #list of roles available to assign via bot


#help document
embed = discord.Embed(title="RotorBot Help", colour=discord.Colour(0x29aaca), description="this is the help document for RotorBot version 0.6")
embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
embed.set_author(name="RotorBot", url="https://github.com/NordicSnow/RotorBot", icon_url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
embed.set_footer(text="rotorbot v0.6", icon_url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
embed.add_field(name="Role Picker", value="To pick roles, use the '+addcar' command followed by one of these options:\n***SA***\n***FB***\n***FC***\n***FD***\n***RX-8***\n***MX-5***")
embed.add_field(name="Image Linker", value="To link a user image, just type in a '+' followed by their username, eg '+nordic'.\nFor a full list of usernames and descriptions, check out http://zekial.io/data.json\nIf you would like yours added, please contact Nordic with a picture and description.")
embed.add_field(name="Image Assigner", value="To add or edit a user image saved in the image linker, use the command '+addimage [direct imgur link] " + '"[description]"' +"'. Make sure to take note of the quotes on the description, which are required.")

#shows console ready message and changes game status
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(activity=discord.Game(name='with ignition timing'))

#welcomes users, mentions them to grab attention, and points them to the welcome channel
@client.event
async def on_member_join(member):
    await client.wait_until_ready()
    channel = client.get_channel(312216330604642305)
    await channel.send('Hello '+ member.mention +', Welcome to the RX-7 Discord Server! We hope you have a great experience! :wink: \nRemember to read ' + '<#333542287256846348>, and if you have any questions feel free to contact the mod team!')


@client.event
async def on_message(message):
    text = message.content.split()
    if message.author == client.user: # prevents recursive loop
        return
    if message.content == "": #ignores messages with only images in them
        return
    

    #role assign
    if message.content[:7] == '+addcar':#checks if addcar command is inputed

        #todo: make this section less of a bodge
        if message.content[8:].upper() == "RX8": #checks if command is "rx8", as the actual name of the role is "RX-8"
            role = discord.utils.get(message.guild.roles, name="RX-8") #gets role ID from server
            await message.channel.send("~role RX-8 added! welcome! ≧◡≦ <3")

        if message.content[8:].upper() == "MX5":#checks if command is "mx5", as the actual name of the role is "RX-8"
            role = discord.utils.get(message.guild.roles, name="MX-5") #gets role ID from server
            await message.channel.send("~role MX-5 added! welcome! ≧◡≦ <3")

        #Assigns roles. Add options to "roleList"
        for i in range(len(roleList)):
            if (message.content[8:].upper()) == roleList[i]: #checks input against list "roleList"
                role = discord.utils.get(message.guild.roles, name=roleList[i]) #gets role ID from server
                await message.channel.send("~role " +roleList[i] + " added! welcome! ≧◡≦ <3")

        try:
            await message.author.add_roles(role) #assigns role to user
        except UnboundLocalError: #if role doesn't exist, this exception is thrown
            await message.channel.send("~i've encountered an error, senpai! try assigning a role that exists! (>人<)\n*for a list of available roles, type in '+help'!* (^ｰ^)") #informs user there was a problem
    

    #add image command
    elif text[0].lower() == '+addimage': #checks to see if command is invoked
        imgur = text[1] #pulls second word from command
        descList = re.findall(r'"([^"]*)"', message.content) #regex to check for words in quotes to pull description data
        
        try:
            desc = descList[0] #makes sure inputed data includes description in quotes
        except IndexError: #handles error and informs user
            await message.channel.send("~uh oh! i've encountered a syntax error! (¤﹏¤)\nremember, "+message.author.name+", the command goes '+addimage [direct imgur link] " + '"[description]"' +"'")
            return #ends add image command to prevent exceptions from occuring due to bad data
        
        if imgur[:20] != "https://i.imgur.com/": #checks to make sure that user is linking from the correct place, and informs them if not
            await message.channel.send("~uh oh! i've encountered a syntax error! (¤﹏¤)\nremember, "+message.author.name+", the link must be directly to the image (from 'i.imgur.com', not just 'imgur.com'). Ping Nordic for help!")
            return #ends add image command to prevent exceptions from occuring due to bad data

        
        with open('data.json') as f: #loads local JSON file
            data = json.load(f) #decodes data into dict
        
        checkVal = False #creates a check value to determine if user is unique
        for i, info in enumerate(data, start=0):  #iterates JSON object names 
            if message.author.id == info["id"]: #detects if an entry matches the username of the invoker
                checkVal = True #if so, the check value is assigned to true to indicate the user is returning
                data[i]['description'] = desc #assigns new description to user's information
                data[i]['link'] = imgur #assigns new image link to user's information
                
                with open('data.json', 'w') as json_file: #opens json file in write mode
                    json.dump(data, json_file, indent = 4, sort_keys=True) #writes data to file and formats it
                await message.channel.send("~~thank you!!! ^>^\nyour data has been updated! have a nice day! {◕ ◡ ◕}") #sends confirmation
        if checkVal == False: #if user doesn't exist, then this value is still set to false
            await message.channel.send("hmm, i can't seem to find a record on you. let me create one real quick... ╰(◡‿◡✿╰)") #sends error message
            data.append({'description': desc, 'link': imgur, 'id': message.author.id, 'username': message.author.name.lower()})
            try:
                with open('data.json', 'w') as json_file:
                        json.dump(data, json_file, indent = 4, sort_keys=True)
                await message.channel.send("~~lovely. i created a record and added in your information! have a nice day! (^▽^)") #sends sucess message
            except:
                await message.channel.send("something went wrong!!! please contact an administrator.") #sends failure message

    #help command
    elif message.content.lower() == "+help": #checks if user typed in help command
            await message.channel.send("~this is what you need to say to control me, master (´･ω･`)")
            await message.channel.send(embed=embed) #sends help documentation embed

    elif message.content.lower() == "+lewd": #checks if user typed in help command
            await message.channel.send("this command exists. idk what to do with it yet tho.")

    #Image Link Handler v0.4 - now ignores case
    firstLetter = message.content[0] #checks if first letter of a message is the invoking one. Can be configured from here.
    if firstLetter == "+": #if not invoking, request is thrown out
        
        with open('data.json') as f:
            data = json.load(f)
        #with urllib.request.urlopen("http://zekial.io/data.json") as url: #opens JSON file from remote webserver
            #data = json.loads(url.read().decode()) #reads and decodes JSON into nested dictionary
        for i, info in enumerate(data, start=0):  #iterates JSON object names 
            testCase = firstLetter + data[i]['username'] #concatonates name with a leading "+" that is part of the invoking letter. Can be configured using the firstLetter variable.
            if (message.content.lower()) == (testCase): #detects if an entry matches the invoked command
                response = data[i]['description'] + "\n" + data[i]['link'] #creates text to be sent involving saved data
                await message.channel.send(response) #transmits data
    
   



    
#run command
client.run(token)