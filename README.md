# RotorBot v0.9

## If you just want to add the car linking to your server, you can use the [version I host here](https://discordapp.com/api/oauth2/authorize?client_id=667799244987695104&permissions=268815424&scope=bot)

## prereqs: [discord.py](https://github.com/Rapptz/discord.py), [requests](https://github.com/psf/requests), SQLite

a discord bot that replies image links and descriptions. designed to be used for hosting image links and descriptions of user's cars. command names, descriptions, and image links are imported from a local SQLite database.

Users can also upload their own image and description using the built-in command, as well as modify them. Images are hosted and served locally.

Finally, it does super basic functionality like role assigning and welcoming users to the server.

## Setup to host yourself:
first, install discord py and pillow

```
python3 -m pip install -U discord.py
```
```
python3 -m pip install -U pillow
```

next, open up "config.json" and input a discord token ([gotten from here](https://discordapp.com/developers/applications/)). If you want to do role assignments and welcome messages through rotorbot, add in your server ID and a channel for welcome messages to go into. If you already have another bot doing that task, just leave it with it's default value. For servers using the version hosted by Nordic, these functions are disabled already. If you want to change what roles you can assign, you can modify them in the "roles" list in "rotorbot.py"

Finally, in a terminal type in "python3 rotorbot.py" and smell the roses.

## HELP
### I'm having import errors!

Some OS installs don't include SQLite or the Python Requests library. Install those and it should work fine.


### where do i get support?

check out the [r/rx7 discord](https://discord.gg/Aut8TAV)



## Licence:

There is no licence. Steal what you want i don't care, nothing in here is useful in any way.
