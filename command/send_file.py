from discord.ext.commands import *
from discord import *

async def setup(bot:Bot):

    @bot.command()
    async def send_file(ctx,file_name):
        await ctx.reply(file=File(fp=f'{file_name}'))