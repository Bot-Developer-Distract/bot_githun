import discord
from discord.ext import commands
import aiohttp
import io
import json
class Videofb(commands.Cog):
    config = {
        "name": "fbvideo",
        "use": "<prefix>fbvideo <link>",
        "desc": "download video facebook",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def videofb(self, ctx, url: str = None):
        try:
            if url == None:
                await ctx.send("Bạn chưa nhập link video facebook muốn download")
                return
            send = await ctx.send("Đang tải video, vui lòng đợi.....")
            async with aiohttp.ClientSession() as session:
                get = await session.get(f"https://docs-api.nguyenhaidang.ml/facebook/video?url={url}")
                get = json.loads(await get.text())
                get2 = await session.get(get["sd"])
                get2 = await get2.read()
                file = discord.File(io.BytesIO(get2), filename="video.mp4")
                await send.delete()
                await ctx.reply("video của bạn đây",file=file)
        except Exception as e:
            print(e)
            await ctx.send("Đã xảy ra lỗi trong quá trình thực hiện:(((video quá nặng hoặc link lỗi)")
async def setup(bot):
    await bot.add_cog(Videofb(bot))
