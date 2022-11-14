import discord
from discord.ext import commands
import aiohttp
import json
import random
import asyncio
import aiofiles
class Vuatiengviet(commands.Cog):
    config = {
        "name": "vuatiengviet",
        "desc": "Game show vua tiếng việt trên discord:)",
        "use": "<prefix>vuatiengviet",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def vuatiengviet(self, ctx):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://raw.githubusercontent.com/undertheseanlp/dictionary/master/dictionary/words.txt') as word:
                    vn_dict = []
                    word = await word.text()
                    word = word.split('\n')
                    for i in word:
                        try:
                            text = json.loads(i)['text']
                            if len(text.split(' ')) == 2:
                                vn_dict.append(text)
                        except:
                            continue
                    random_word = random.choice(vn_dict)
                async with session.get(f'https://api.phamvandien.xyz/vuatiengviet/image?word={random_word}') as resp:
                    f = await aiofiles.open('vuatiengviet.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
                    send = await ctx.send('====Vua Tieng Viet====\nday la cau hoi cua ban:\nreply tin nhan nay de tra loi, ban co 45 giay de tra loi', file = discord.File('vuatiengviet.png'))
                    def check(m):
                        return m.author.id == ctx.author.id and m.channel == ctx.channel and m.reference is not None and m.reference.message_id == send.id
                    try:
                        message = await self.bot.wait_for('message', timeout=45, check=check)
                        if message:
                            if str(message.content).lower() == str(random_word).lower():
                                await ctx.send(f'bạn đã trả lời đúng, đáp án là "{random_word}"')
                            else:
                                await ctx.send(f'sai rồi đáp án là "{random_word}"')
                    except asyncio.TimeoutError:
                        await ctx.send('Hết giờ!')
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Vuatiengviet(bot))
