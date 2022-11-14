from distutils.util import change_root
from discord.ext import commands
from discord import *
import io,aiohttp,time,random,datetime
import json
class Welcome(commands.Cog):
    config = {
        "name": "set_welcome",
        "desc": "Tự động chào đón người dùng mới",
        "use": "tự động trả lời khi nhắn tin ở kênh đã cài đặt",
        "author": "King.(maku team)",
        "event": False
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_member_join(self,member):
        self.bot.sql.execute(f'SELECT server_channel_simimi FROM server_data WHERE server_id={message.guild.id}')
        if (self.bot.sql.fetchone() == None):
            self.bot.sql.execute(f'INSERT INTO server_data (server_id,server_prefix,server_channel_simimi,server_channel_confession,server_channel_welcome) VALUES ({message.guild.id},0,0,0,0)')
        else:
            self.bot.sql.execute(f'SELECT server_channel_simimi FROM server_data WHERE server_id={message.guild.id}')
            channel_welcome = self.bot.get_channel(self.bot.sql.fetchone()[0])
            em = Embed(title="chào bạn đã đến với server",description='chào and nothing',colour=0xFFFFF)
            await channel_welcome.send(content=f"{member.mention}",embed=em)
    @commands.command()
    async def set_welcome(ctx,self,channel_welcome):
        self.bot.sql.execute(f'SELECT server_channel_simimi FROM server_data WHERE server_id={message.guild.id}')
        if (self.bot.sql.fetchone() == None):
            self.bot.sql.execute(f'INSERT INTO server_data (server_id,server_prefix,server_channel_simimi,server_channel_confession,server_channel_welcome) VALUES ({message.guild.id},0,0,0,0)')
        else:
            self.bot.sql.execute(f'UPDATE server_data SET server_channel_welcome = {channel_welcome} where server_id = {ctx.guild.id}')
async def setup(bot):
    await bot.add_cog(Welcome(bot))
