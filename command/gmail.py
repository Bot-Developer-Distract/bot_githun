import discord
from discord.ext import commands
import requests,aiohttp
class Gmail(commands.Cog):
    config = {
        "name": "temp gmail",
        "desc": "tạo gmail ảo",
        "use": "<prefix>gmail",
        "author": "King.(maku team)",
        "event": False
    }
    def __init__(self, bot):
        self.bot = bot
        self.bot.session = aiohttp.ClientSession()
    @commands.command()
    async def gmail(self,ctx):
        try:
            async with self.bot.session.get(f'https://api-iotran.tk/get-mail') as get_request_mail:
                get_mail = await get_request_mail.json()
                em = discord.Embed(title='Tạo gmail thành công',description=f'gmail :{get_mail["gmail"]}\ncode :{get_mail["code"]}',color=0xFFFFF)
                user = await self.bot.fetch_user(ctx.message.author.id)
                await user.send(embed=em)
        except Exception as e:
            print(e)
            


async def setup(bot):
    await bot.add_cog(Gmail(bot))
