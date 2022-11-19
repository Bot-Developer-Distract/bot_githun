from discord.ext import commands
import discord
class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def avatar(self, ctx, member: discord.User = None):
        if member == None:
            await ctx.send(ctx.author.display_avatar.url)
            return
        await ctx.send(member.display_avatar.url)
async def setup(bot):
    await bot.add_cog(Avatar(bot))
