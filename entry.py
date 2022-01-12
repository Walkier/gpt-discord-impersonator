from discord.ext import commands

from FacelessBot import FacelessBot
from register import register_commands

from keys import Keys

bot = FacelessBot(command_prefix='.') #super = (discord.ext.commands.Bot, discord.Client)

register_commands(bot)

bot.run(Keys.TOKEN)
