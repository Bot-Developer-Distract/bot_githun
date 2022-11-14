import discord
from discord.ext import commands
import easy_pil
import aiofiles
import aiohttp
import asyncio
class Coffee_dog(commands.Cog):
    config = {
        "name": "dog_coffee",
        "desc": "Hình ảnh mô tả một chú chó:))",
        "use": "<prefix>dog_coffee @mention",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def dog_coffee(self, ctx, member: discord.User = None):
        try:
            if member == None:
                image = await easy_pil.load_image_async(ctx.author.display_avatar.url)
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://i.ibb.co/T0XqWkt/paste.jpg') as resp:
                        f = await aiofiles.open('paste.jpg', mode='wb')
                        await f.write(await resp.read())
                        await f.close()
                back = easy_pil.Editor('paste.jpg')
                paste = easy_pil.Editor(image).circle_image()
                paste.resize((220, 220))
                back.paste(paste, (305, 85))
                file = discord.File(fp=back.image_bytes, filename='circle.png')
                async with ctx.typing():
                    await asyncio.sleep(4)
                await ctx.send(f"Khoẻ ko em:)) <@{ctx.message.author.id}>",file=file)
            else:
                image = await easy_pil.load_image_async(member.display_avatar.url)
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://i.ibb.co/T0XqWkt/paste.jpg') as resp:
                        f = await aiofiles.open('paste.jpg', mode='wb')
                        await f.write(await resp.read())
                        await f.close()
                back = easy_pil.Editor('paste.jpg')
                paste = easy_pil.Editor(image).circle_image()
                paste.resize((220, 220))
                back.paste(paste, (305, 85))
                file = discord.File(fp=back.image_bytes, filename='circle.png')
                async with ctx.typing():
                    await asyncio.sleep(4)
                await ctx.send('Khoẻ ko em:)) <@{member.id}>',file=file)
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Coffee_dog(bot))
