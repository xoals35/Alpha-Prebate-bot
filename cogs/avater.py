import discord
import asyncio
from discord.ext import commands


class avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def 프사(self, ctx, member : discord.Member = None):

        if member is None:
            embed = discord.Embed(title="이 명령은 다음과 같이 사용됩니다.: ```s!프사 (맨션)```", colour=0xff0000, timestamp=ctx.message.created_at)
            await ctx.send(embed=embed)
            return

        else:
            embed2 = discord.Embed(title=f"{member}님의 프사 입니다.", colour=0x0000ff, timestamp=ctx.message.created_at)
            embed2.add_field(name="Animated?", value=member.is_avatar_animated())
            embed2.set_image(url=member.avatar_url)
            await ctx.send(embed=embed2)


def setup(bot):
    bot.add_cog(avatar(bot))