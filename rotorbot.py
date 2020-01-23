# dependencies 
import os
from array import *
import urllib.request, json
import discord
from discord.ext import commands

#bot token
token = '<insert token here>' #this should be in a seperate file but its not public so who cares

client = discord.Client()
defaultChannel = client.get_channel(312216330604642305)

#shows console ready message and changes game status
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(activity=discord.Game(name='with apex seals'))

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
    firstLetter = message.content[0] #checks if first letter of a message is the invoking one. Can be configured from here.
    if firstLetter == "+": #if not invoking, request is thrown out
        with urllib.request.urlopen("http://zekial.io/data.json") as url: #opens JSON file from remote webserver
            data = json.loads(url.read().decode()) #reads and decodes JSON into nested dictionary
        for name, info in data.items():  #iterates JSON object names 
            testCase = firstLetter + name #concatonates name with a leading "+" that is part of the invoking letter. Can be configured using the firstLetter variable.
            if message.content == (testCase): #detects if an entry matches the invoked command
                response = data[name]['description'] + "\n" + data[name]['link'] #creates text to be sent involving saved data
                await message.channel.send(response) #transmits data

#run command
client.run(token)