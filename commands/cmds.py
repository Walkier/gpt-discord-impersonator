import discord
from discord.ext import commands
from FacelessBot import FacelessBot

@commands.command()
async def status(ctx):
    bot: FacelessBot = ctx.bot 
    bot.log_command(ctx)

    pretender = bot.pipe_convo
    await bot.reply(ctx.channel, f"wait sec: {pretender._buffer_secs}\nmodel: {pretender._run_name}_{pretender._checkpoint}\n" + \
        f"target: {pretender._pretend_target}\ntarget's new name: {pretender._pretend_target_target}\nmessage read num bf reply: {pretender._msg_history_len}")

@commands.command()
async def change_target(ctx, target):
    bot: FacelessBot = ctx.bot 
    bot.log_command(ctx)

    bot.pipe_convo._pretend_target = target
    if ctx.message.guild:
        await ctx.message.guild.get_member(bot.user.id).edit(nick=target)
    await bot.reply(ctx.channel, f'new target {bot.pipe_convo._pretend_target}')

    await bot.change_presence(activity = discord.Game(name=f'{bot.pipe_convo._pretend_target}'))

@commands.command(brief='type .help change_target_target', description="change the username of the person it is pretending (from the bot's perspective). allows you to talk to yourself better.")
async def change_target_target(ctx, target):
    bot: FacelessBot = ctx.bot 
    bot.log_command(ctx)

    bot.pipe_convo._pretend_target_target = target
    await bot.reply(ctx.channel, f'the bot will now see {bot.pipe_convo._pretend_target} as {bot.pipe_convo._pretend_target_target}')

__all__ = [status, change_target, change_target_target]
