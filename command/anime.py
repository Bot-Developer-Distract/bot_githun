import discord
from discord.ext import commands
import aiohttp
import json
import random
from command.random_list import list_color
class Anime(commands.Cog):
  config = {
      "name": "anime",
      "desc": "gif anime theo từng category+)",
      "use": "<prefix>anime <category>\ncác category hiện có: baka, bite, blush, bored, cry, cuddle, dance, facepalm, feed, handhold, happy, highfive, hug, kick,kiss, laugh, pat, poke, pout, punch, shoot, shrug, slap, sleep, smile, smug, stare, think, thumbsup, tickle, wave, wink, yeet",
      "author": "Anh Duc(aki team)"
    }
  def __init__(self, bot):
    self.bot = bot
  @commands.command()
  async def anime(self, ctx, category = None):
    try:
        if category== None:
            await ctx.send("bạn chưa nhập category")
            return
        async with aiohttp.ClientSession() as session:
            get = await session.get(f"https://nekos.best/api/v2/{category}?amount=1")
            data = await get.json()
            if get.status == 200:
                gif = data["results"][0]["url"]
                em_load = discord.Embed(colour = random.choice(list_color))
                em_load.set_image(url = gif)
                await ctx.reply(embed = em_load)
                return
            await ctx.send("error")
    except Exception as e:
      print(e)
async def setup(bot):
  await bot.add_cog(Anime(bot))
