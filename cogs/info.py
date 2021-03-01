from datetime import datetime
from typing import Optional

from discord import Embed, Member
from discord.ext.commands import Cog
from discord.ext.commands import command

class Info(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="userinfo", aliases=["유저정보", "ui", "mi"])
	async def user_info(self, ctx, target: Optional[Member]):
		target = target or ctx.author

		embed = Embed(title="유저 info",
					  colour=target.colour,
					  timestamp=datetime.utcnow())

		embed.set_thumbnail(url=target.avatar_url)

		fields = [("이름", str(target), True),
				  ("아이디", target.id, True),
				  ("봇?", target.bot, True),
				  ("최고 역할", target.top_role.mention, True),
				  ("상태", str(target.status).title(), True),
				  ("활동", f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}", True),
				  ("계정 생성일", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("서버 들어온날짜", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("부스트", bool(target.premium_since), True)]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		await ctx.send(embed=embed)

	@command(name="serverinfo", aliases=["서버정보", "si", "gi"])
	async def server_info(self, ctx):
		embed = Embed(title="서버 info",
					  colour=ctx.guild.owner.colour,
					  timestamp=datetime.utcnow())

		embed.set_thumbnail(url=ctx.guild.icon_url)

		statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

		fields = [("아이디", ctx.guild.id, True),
				  ("서버 오너", ctx.guild.owner, True),
				  ("지역", ctx.guild.region, True),
				  ("서버 생일", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("멤버", len(ctx.guild.members), True),
				  ("사람", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
				  ("봇", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
				  ("차단 된 멤버", len(await ctx.guild.bans()), True),
				  ("상태", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
				  ("채팅채널", len(ctx.guild.text_channels), True),
				  ("보이스채널", len(ctx.guild.voice_channels), True),
				  ("카테고리", len(ctx.guild.categories), True),
				  ("역할", len(ctx.guild.roles), True),
				  ("초대", len(await ctx.guild.invites()), True),
				  ("\u200b", "\u200b", True)]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		await ctx.send(embed=embed)

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("info")


def setup(bot):
	bot.add_cog(Info(bot))