from discord.ext.commands import bot

from commands import cmds, gpt_commands
from commands.debug import debug

def register_commands(bot: bot):
    directory = [
        debug,
        *cmds.__all__,
        *gpt_commands.__all__,
    ]

    for command in directory:
        bot.add_command(command)
