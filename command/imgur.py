import discord
from discord.ext import commands
import aiohttp
class Imgur(commands.Cog):
    config = {
        "name": "imgur",
        "desc": "upload image to imgur",
        "use": "<prefix>imgur",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def imgur(self, ctx):
        if ctx.message.attachments:
            for i in ctx.message.attachments:
                async with aiohttp.ClientSession() as session:
                    get = await session.get(f"https://api-thanhali.thanhali.repl.co/imgur?link={i.url}")
                    get = await get.json()
                    if get['uploaded']['status'] == "success":
                        await ctx.reply(f"upload ảnh thành công\nlink: {get['uploaded']['image']}")
                        return 
                    await ctx.send('Error: Upload ảnh thất bại')
            return
        await ctx.send("Hãy gửi kèm theo các bức ảnh bạn muốn đăng lên imgur")
async def setup(bot):
    await bot.add_cog(Imgur(bot))
