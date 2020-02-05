# libraries
import os, re, discord, discord.utils, sqlite3, os.path, requests, json
from discord.ext import commands

#db connection
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #directs to exact file
db_path = os.path.join(BASE_DIR, "imagestore.db") #database name configured here
conn = sqlite3.connect(db_path, isolation_level=None) #set to apply changes on execution
c = conn.cursor()

#bot tokens
token = '<insert discord bot token here>' #discord api client token
clientID='<insert imgur app client ID here>' #imgur api client ID

client = discord.Client() #client object

roleList = ["SA", "FB", "FC", "FD", "RX-8", "MX-5"] #list of roles available to assign via bot


#help document
embed = discord.Embed(title="RotorBot Help", colour=discord.Colour(0x29aaca), description="this is the help document for RotorBot version 0.7")
embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
embed.set_author(name="RotorBot", url="https://github.com/NordicSnow/RotorBot", icon_url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
embed.set_footer(text="rotorbot v0.7", icon_url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
embed.add_field(name="Role Picker", value="To add a new role, use the '+addcar' command followed by one of these options:\n***SA***\n***FB***\n***FC***\n***FD***\n***RX-8***\n***MX-5***")
embed.add_field(name="Show an image of a user's car", value="To see a given user's car, just type in a '+' followed by their username, eg '+nordic'.")
embed.add_field(name="Add yourself to the image linker", value="To add or edit a user image saved in the image linker, use the command '+addimage " + '"[description]"' +"' and attach your image to the message. Make sure to take note of the quotes on the description, which are required.")

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
    uid = (message.author.id,)
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
        
        if message.attachments == []: #checks to make sure that user has included an attachment, and informs them if not
            await message.channel.send("~uh oh! there isn't an image for me to upload\nremember, "+message.author.name+", the image has to be attached to the invoking message!")
            return #ends add image command to prevent exceptions from occuring due to bad data


        response = requests.post('https://api.imgur.com/3/upload', data={'image':message.attachments[0].url}, headers={'Authorization': ('Client-ID ' + clientID)}) #uploads attachment URL to imgur
        if str(response) == "<Response [200]>": #checks if upload suceeded
            jsonData = response.json() #reads json data from response

            c.execute('SELECT * FROM images WHERE UID =?', uid) #pulls user information
            currentData = (c.fetchone())
            if currentData == None: #checks to see if user exists in the database
                await message.channel.send("hmm, i can't seem to find a record on you. let me create one real quick... ╰(◡‿◡✿╰)") #sends error message
                c.execute('INSERT INTO images VALUES (?,?,?,?)', (message.author.name.lower(), message.author.id, desc, jsonData['data']['link'])) #creates new values using user account and provided information
                await message.channel.send("~~lovely. i created a record and added in your information! have a nice day! (^▽^)") #sends sucess message
            else:
                c.execute('UPDATE images SET description = ?, link = ? WHERE uid = ? ', (desc, jsonData['data']['link'], message.author.id)) #updates existing information
                await message.channel.send("~~thank you!!! ^>^\nyour data has been updated! have a nice day! {◕ ◡ ◕}") #sends confirmation
        else: #if upload isn't sucessful, throws an error
            await message.channel.send("Error! Imgur Upload Failed! Either Imgur is down or there is a problem with your image.\nfor debugging: http " + str(response)) #sends confirmation

    #help command
    elif message.content.lower() == "+help": #checks if user typed in help command
            await message.channel.send("~this is what you need to say to control me, master (´･ω･`)")
            await message.channel.send(embed=embed) #sends help documentation embed

    elif message.content.lower() == "+iq": #checks if user has indicated they are dealing with a low IQ individual
            await message.channel.send("To be fair, you have to have a very high IQ to drive an FD RX-7.The car is extremely superior to any other modern supercar, and without a solid grasp of theoretical physics you can't even drive it. There's also it’s linear power delivery, which is deftly woven into it’s driving characterisation- it’s personal philosophy draws heavily from Italian designs, for instance. I personally understand this stuff; I have the intellectual capacity to truly appreciate the supreme handling, to realise that it’s not just good- it says something deep about LIFE. As a consequence people who dislike the FD truly ARE idiots- of course they wouldn't appreciate, for instance, the humour in the FD’s existential catchphrase “Boost in, Apex Seals out,” which itself is a cryptic reference to the tenuous balance between life and death. I'm smirking right now just imagining one of those addlepated simpletons scratching their heads in confusion as Yoichi Sato's genius design unfolds itself on the race track. What fools.. how I pity them. :joy: And yes, by the way, i DO have a FD tattoo. And no, you cannot see it. It's for the ladies' eyes only- and even then they have to demonstrate that they're within 5 IQ points of my own (preferably lower) beforehand. Nothin personnel kid :sunglasses:")
    
    '''elif message.content.lower() == "gapplebees": #checks if user has typed in a stale maymay
            await message.channel.send("DANGER!!! DANGEROUSLY UNFUNNY MEME DETECTED!!! EXTREME CAUTION ADVISED!!")'''
    #Image Link Handler v0.4 - now ignores case
    firstLetter = message.content[0] #checks if first letter of a message is the invoking one. Can be configured from here.
    if firstLetter == "+": #if not invoking, request is thrown out
        
        commandName = (message.content.lower()[1:],) # checks command name
        c.execute('SELECT * FROM images WHERE Username =?', commandName) #compares command name amoung populated users
        currentData = (c.fetchone())
        if currentData == None: #if no user exists, command ends
            return
        else:
            await message.channel.send(currentData[2] + "\n" + currentData[3]) #otherwise, information from DB is supplied.
            
#run command
client.run(token)