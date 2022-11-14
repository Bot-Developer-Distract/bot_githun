import discord
from discord.ext import commands
import json
import aiofiles
import aiohttp
import sys
import requests
import random
import io
import main
import random
from command.random_list import list_color
import aiofiles
class Dhbc(commands.Cog):
    config = {
        "name": "dhbc",
        "desc": "Game đuổi hình bắt chữ",
        "use": "<prefix>dhbc",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def dhbc(self, ctx):
        try:
            self.bot.sql.execute(f'SELECT user_money FROM user_data WHERE user_id={ctx.author.id}')
            money = self.bot.sql.fetchone()[0]
            async with aiohttp.ClientSession() as session:
                api = ['https://api.phamvandien.xyz/game/dhbcv1', 'https://www.nguyenmanh.name.vn/api/dhbc1?apikey=KCL98tNB', 'https://docs-api.nguyenhaidang.ml/game/dhbc']
                get = random.choice(api)
                question = await session.get(get)
                question = json.loads(await question.text())
                if get == api[0]:
                    get = await session.get(question["dataGame"]['link'])
                    em = discord.Embed(title="_==== Đuổi Hình Bắt Chữ====_", description='đây là câu hỏi của bạn:\nreply tin nhắn này để trả lời câu hỏi và reply "gợi ý" để lấy gợi ý câu trả lời (50$/lần)', color = random.choice(list_color))
                    file = discord.File(io.BytesIO(await get.read()), filename="dhbc.png")
                    em.set_image(url = "attachment://dhbc.png")
                    send = await ctx.send(embed=em, file = file)
                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel and m.reference is not None and m.reference.message_id == send.id
                    message = await self.bot.wait_for('message', check = check, timeout=45)
                    if str(message.content).lower() == "gợi ý":
                        self.bot.sql.execute(f'SELECT user_money FROM user_data WHERE user_id={ctx.author.id}')
                        money = self.bot.sql.fetchone()[0]
                        if int(money) < 50:
                            await ctx.send('bạn không đủ 50$ trong ví để xem gợi ý')
                            message = await self.bot.wait_for('message', check = check, timeout=45)
                            if str(message.content).lower() == str(question['dataGame']['tukhoa']).lower():
                                await ctx.send(f'bạn đã trả lời đúng, đáp án là: "{question["dataGame"]["tukhoa"]}"')
                            else:
                                await ctx.send(f"sai rồi:(, đáp án đúng là: {question['dataGame']['tukhoa']}")
                        else:
                            await main.update(ctx.author.id, 50, "lose_wallet")
                            await ctx.send(f'gợi ý, từ này là: {question["dataGame"]["suggestions"]}')
                            message = await self.bot.wait_for('message', check = check, timeout=45)
                            if str(message.content).lower() == str(question['dataGame']['tukhoa']).lower():
                                await ctx.send(f'bạn đã trả lời đúng, đáp án là: "{question["dataGame"]["tukhoa"]}"')
                            else:
                                await ctx.send(f"sai rồi:(, đáp án đúng là: {question['dataGame']['tukhoa']}")
                    else:
                        if str(message.content).lower() == str(question['dataGame']['tukhoa']).lower():
                            await ctx.send(f"Bạn đã trả lời đúng, đáp án là {question['dataGame']['tukhoa']}")
                        else:
                            await ctx.send(f"sai rồi:(, đáp án đúng là: {question['dataGame']['tukhoa']}")
                if get == api[1]:
                    get = await session.get(question['result']['link'])
                    em = discord.Embed(title="_==== Đuổi Hình Bắt Chữ====_", description='đây là câu hỏi của bạn:\nreply tin nhắn này để trả lời câu hỏi và reply "gợi ý" để lấy gợi ý câu trả lời (50$/lần)', color = random.choice(list_color))
                    file = discord.File(io.BytesIO(await get.read()), filename="dhbc.png")
                    em.set_image(url = "attachment://dhbc.png")
                    send = await ctx.send(embed=em, file = file)
                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel and m.reference is not None and m.reference.message_id == send.id
                    message = await self.bot.wait_for('message', check = check, timeout=45)
                    if str(message.content).lower() == "gợi ý":
                        
                        if int(money) < 50:
                            await ctx.send('bạn không đủ 50$ trong ví để xem gợi ý')
                            message = await self.bot.wait_for('message', check = check, timeout=45)
                            if str(message.content).lower() == str(question['result']['tukhoa']).lower():
                                await ctx.send(f'bạn đã trả lời đúng, đáp án là: "{question["result"]["tukhoa"]}"')
                            else:
                                await ctx.send(f"sai rồi:(, đáp án đúng là: {question['result']['tukhoa']}")
                        else:
                            await main.update(ctx.author.id, 50, "lose_wallet")
                            await ctx.send(f'gợi ý, từ này là: {question["result"]["suggestions"]}')
                            message = await self.bot.wait_for('message', check = check, timeout=45)
                            if str(message.content).lower() == str(question['result']['tukhoa']).lower():
                                await ctx.send(f'bạn đã trả lời đúng, đáp án là: "{question["result"]["tukhoa"]}"')
                            else:
                                await ctx.send(f"sai rồi:(, đáp án đúng là: {question['result']['tukhoa']}")
                    else:
                        if str(message.content).lower() == str(question['result']['tukhoa']):
                            await ctx.send(f"Bạn đã trả lời đúng, đáp án là {question['result']['tukhoa']}")
                        else:
                            await ctx.send(f"sai rồi:(, đáp án đúng là: {question['result']['tukhoa']}")
                if get == api[2]:
                    get = await session.get(question['image1and2'])
                    em = discord.Embed(title="_==== Đuổi Hình Bắt Chữ====_", description='đây là câu hỏi của bạn:\nreply tin nhắn này để trả lời câu hỏi', color = random.choice(list_color))
                    file = discord.File(io.BytesIO(await get.read()), filename="dhbc.png")
                    em.set_image(url = "attachment://dhbc.png")
                    send = await ctx.send(embed=em, file = file)
                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel and m.reference is not None and m.reference.message_id == send.id
                    message = await self.bot.wait_for('message', check = check, timeout=45)
                    if 1 == 2:
                        print(9)
                    else:
                        if str(message.content).lower() == str(question['wordcomplete']).lower():
                            await ctx.send(f"Bạn đã trả lời đúng, đáp án là {question['wordcomplete']}")
                        else:
                            await ctx.send(f"sai rồi:(, đáp án đúng là: {question['wordcomplete']}")
        except Exception as e:
            print(e)
            await ctx.send('error')
async def setup(bot):
    await bot.add_cog(Dhbc(bot))
