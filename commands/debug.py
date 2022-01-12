from discord.ext import commands

@commands.command()
async def debug(ctx):
    ctx.bot.log_command(ctx)

    if ctx.author.name == "Walkier" and ctx.author.discriminator == "4488":
        print('debug invoked')
        breakpoint()
