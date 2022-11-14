from discord.ext import commands
import discord
import io,aiohttp,time,random,datetime,os,sys
import json
class Restart(commands.Cog):
    config = {
        "name": "restart",
        "desc": "Khởi động lại bot",
        "use": "<prefix>restart",
        "author": "King.(maku team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def restart(self,ctx):
        await ctx.reply("Đang khởi động lại bot,xin hãy đợi")
        #fixing...
    


async def setup(bot):
    await bot.add_cog(Restart(bot))
