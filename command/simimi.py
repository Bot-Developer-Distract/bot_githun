from discord.ext import commands
from discord import *
import io,aiohttp,time,random,datetime
import json
class Simimi(commands.Cog):
    config = {
        "name": "simimi",
        "desc": "nói chuyện với trợ lý simimi",
        "use": "tự động trả lời khi nhắn tin ở kênh đã cài đặt",
        "author": "King.(maku team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_message(self,message):
        try:
            if message.author.id != 1014185794396762132:
                self.bot.sql.execute(f'SELECT server_channel_simimi FROM server_data WHERE server_id={message.guild.id}')
                if (self.bot.sql.fetchone() == None):
                    self.bot.sql.execute(f'INSERT INTO server_data (server_id,server_prefix,server_channel_simimi,server_channel_confession) VALUES ({message.guild.id},0,0,0)')
                else:
                    self.bot.sql.execute(f'SELECT server_channel_simimi FROM server_data WHERE server_id={message.guild.id}')
                    server_channel_simimi = self.bot.sql.fetchone()[0]
                    if message.channel.id == server_channel_simimi:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(f'https://simsimi.info/api/?lc=vi&text={message.content}') as get_answer:
                                get_answer = await get_answer.text()
                                answer =  json.loads(get_answer)
                                if answer["status"] == "success":
                                    await message.reply(answer['message'])
                                else:
                                    await message.reply("oppa nói lại rõ hơn đc khum ạ,em chx hiểu lắm 😳")
                                
    
            self.bot.database.commit()
        except Exception as e:
            print(e)
        
    @commands.command()
    async def simimi(self,ctx,channel_simimi):
        try:
            self.bot.sql.execute(f'UPDATE server_data SET server_channel_simimi ={channel_simimi} WHERE server_id={ctx.guild.id}')
            await ctx.reply(f"Đã đổi channel của simimi sang kênh <#{channel_simimi}>")
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(Simimi(bot))
