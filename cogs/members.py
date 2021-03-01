import discord
import asyncio
from discord.ext import commands



class members(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def 멤버(self, ctx):

        embed = discord.Embed(title=f"{ctx.guild.name}서버에{len(ctx.guild.members)}회원이 있습니다.", colour=0xffff00, timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(members(bot))