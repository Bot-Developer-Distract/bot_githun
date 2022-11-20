import discord
from discord.ext import commands
import aiohttp
import random
from command.random_list import list_color
class Worldcup(commands.Cog):
    config = {
        "name": "worldcup",
        "desc": "xem thong tin ve tran dau world cup moi nhat=))",
        "use": "<prefix>worldcup",
        "author": "aki team"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def worldcup(self, ctx):
        try:
            async with aiohttp.ClientSession() as session:
                data = await session.get("https://api-iotran.tk/worldcup")
                data = await data.json()
                em = discord.Embed(title= "**⚽ Today worldcup match**", color = random.choice(list_color))
                em.add_field(name = "Trận đấu sắp diễn ra:", value=str(data["Trận đấu sắp diễn ra "]))
                em.add_field(name = "trận đấu tại bảng: " , value = data["Bảng"], inline =True)
                em.add_field(name = "bắt đầu vào:", value=f"{data['Ngày diễn ra']} - {data['Thời gian bắt đầu']}")
                em.add_field(name = "Trạng thái trận đấu", value=data["Trạng thái trận đấu"])
                await ctx.reply(embed = em)
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Worldcup(bot))
