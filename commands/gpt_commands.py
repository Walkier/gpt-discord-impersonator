from discord.ext import commands
from FacelessBot import FacelessBot

@commands.command(brief='list all trained conversational models')
async def list_models(ctx: commands.Context):
    bot: FacelessBot = ctx.bot 
    bot.log_command(ctx)

    models = bot.pipe_convo.get_models()

    resp_msg = ''
    for model_name, epochs in models.items():
        resp_msg += f'\n{model_name}:\n'
        for epoch in epochs:
            resp_msg += f'epoch {epoch}\n'

    await bot.reply(ctx.channel, resp_msg)

@commands.command(brief='change conversational model')
async def load_model(ctx: commands.Context, model_name, checkpoint='latest'):
    bot: FacelessBot = ctx.bot 
    bot.log_command(ctx)

    pretender = bot.pipe_convo
    if pretender.change_model(model_name, checkpoint):
        await bot.reply(ctx.channel, f'model changed to {pretender._run_name}, epoch {pretender._checkpoint}')
    else:
        await bot.reply(ctx.channel, f'model not found')

__all__ = [list_models, load_model]