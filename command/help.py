import random
import discord
from discord.ext import commands
class Help(commands.Cog):
    config = {
        "name": "help",
        "desc": "Xem thông tin về các lệnh hiện có trên bot và về bot",
        "use": "<prefix>help <command>",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def help(self, ctx, mdl = None):
        try:
            if mdl == None:
                module = ''
                for i in self.bot.cogs:
                    try:
                        x = self.bot.cogs[i].config.get("event", False)
                        if not x:
                            module += self.bot.cogs[str(i)].config["name"] + '\n'
                    except:
                        continue 
                em = discord.Embed(title="_HELP COMMAND_", description="Sử dụng `<prefix>help <lệnh>` để biết rõ hơn thông tin về lệnh", color=0xFFF)
                em.add_field(name="_Cac lenh hien co tren bot_", value=module)
                em.set_image(url='https://i0.wp.com/www.printmag.com/wp-content/uploads/2021/02/4cbe8d_f1ed2800a49649848102c68fc5a66e53mv2.gif?fit=476%2C280&ssl=1')
                await ctx.send(embed=em)
            else:
                try:
                  msg = self.bot.cogs[str(mdl).lower().capitalize()].config
                  if msg.get("event", False):
                    await ctx.send(str(mdl) + "không phải là một lệnh")
                    return
                  em = discord.Embed(title = f"_{mdl.lower()}_", description=f"Tên lệnh: {msg['name']}\nMô tả: {msg['desc']}\nCách sử dụng: {msg['use']}\ntác giả: {msg['author']}\n")
                  await ctx.send(embed = em)
                except Exception as e:
                    print(e)
                    await ctx.send(f'lệnh {mdl} không tồn tại hoặc chưa được thiết lập cho lệnh help')
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Help(bot))
