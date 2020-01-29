# dependencies 
import os
from array import *
import urllib.request, json
import discord
from discord.ext import commands
import discord.utils


#bot token
token = 'NjY3Nzk5MjQ0OTg3Njk1MTA0.XjHWCQ.XiCyKLghl_EHLmgFSWMxrxuoGFA' #this should be in a seperate file but its not public so who cares

client = discord.Client()
defaultChannel = client.get_channel(312216330604642305)

roleList = ["SA", "FB", "FC", "FD", "RX-8", "MX-5"] #list of roles available to assign via bot

#help document
embed = discord.Embed(title="RotorBot Help", colour=discord.Colour(0x29aaca), description="this is the help document for RotorBot version 0.5")
embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
embed.set_author(name="RotorBot", url="https://zekial.io", icon_url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
embed.set_footer(text="rotorbot v0.5", icon_url="https://cdn.discordapp.com/avatars/667799244987695104/a84e8b9d69329358e9a29b4bfeb8b3ca.png?size=256")
embed.add_field(name="Role Picker", value="To pick roles, use the '+addcar' command followed by one of these options:\n***SA***\n***FB***\n***FC***\n***FD***\n***RX-8***\n***MX-5***")
embed.add_field(name="Image Linker", value="To link a user image, just type in a '+' followed by their username, eg '+nordic'.\nFor a full list of usernames and descriptions, check out http://zekial.io/data.json\nIf you would like yours added, please contact Nordic with a picture and description.")

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
    await channel.send('Hi '+ member.mention +', Welcome to the RX7 Discord! Have a great time here :wink: ! Remember to read ' + '<#333542287256846348>')

#Image Link Handler v0.3
@client.event
async def on_message(message):
    if message.author == client.user: # prevents recursive loop
        return
    if message.content == "": #ignores messages with only images in them
        return
    
    #role assign
    if message.content[:7] == '+addcar':#checks if addcar command is inputed

        #todo: make this section less of a bodge
        if message.content[8:].upper() == "RX8": #checks if command is "rx8", as the actual name of the role is "RX-8"
            role = discord.utils.get(message.guild.roles, name="RX-8") #gets role ID from server
            await message.author.add_roles(role) #adds role to user
            await message.channel.send("~role RX-8 added! welcome! ≧◡≦ <3")

        if message.content[8:].upper() == "MX5":#checks if command is "mx5", as the actual name of the role is "RX-8"
            role = discord.utils.get(message.guild.roles, name="MX-5") #gets role ID from server
            await message.author.add_roles(role) #adds role to user
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
    #help command
    elif message.content.lower() == "+help": #checks if user typed in help command
            await message.channel.send("~this is what you need to say to control me, master (´･ω･`)")
            await message.channel.send(embed=embed) #sends help documentation embed

    firstLetter = message.content[0] #checks if first letter of a message is the invoking one. Can be configured from here.
    if firstLetter == "+": #if not invoking, request is thrown out
        with urllib.request.urlopen("http://zekial.io/data.json") as url: #opens JSON file from remote webserver
            data = json.loads(url.read().decode()) #reads and decodes JSON into nested dictionary
        for name, info in data.items():  #iterates JSON object names 
            testCase = firstLetter + name #concatonates name with a leading "+" that is part of the invoking letter. Can be configured using the firstLetter variable.
            if (message.content.lower()) == (testCase): #detects if an entry matches the invoked command
                response = data[name]['description'] + "\n" + data[name]['link'] #creates text to be sent involving saved data
                await message.channel.send(response) #transmits data
    
   



    
#run command
client.run(token)