from discord.ext import commands
import discord
import aiohttp #sử dụng aiohttp thay cho requests 
class worldcup(commands.Cog):
    config = {
        "name": "...", #tên lệnh
        "desc": "...", #mô tả về lệnh
        "use": "...", #cách sử dụng 
        "author": "...", #credit tác giả
        "event": False #nếu là event thì để True còn là lệnh thì để False hoặc không để gì cũng đc:))
    }
    def __init__(self, bot):
        self.bot = bot
        self.bot.session = aiohttp.ClientSession()
    @commands.command()
    async def worldcup(self,ctx):
        async with self.bot.session.get(f'https://api-iotran.tk/worldcup') as get_answer: #gửi request đến api (có thể đọc docs của aiohttp để biết rõ hơn-))
            answer = await get_answer.json()
            em = discord.embeds.Embed(title="Trận đấu sắp diễn ra",description=f"Đội:{answer['Trận đấu sắp diễn ra']} /n Bảng:{answer['Bảng']} /n Trạng thái trận đấu:{answer['Trạng thái trận đấu']}",color=0x00ff00)
            await ctx.reply(answer)
    


async def setup(bot):
    await bot.add_cog(worldcup(bot))
