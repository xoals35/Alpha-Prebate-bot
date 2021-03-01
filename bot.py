import discord
from discord import message
from discord.enums import _is_descriptor
from discord.ext import commands
import asyncio
import datetime
import random
import time
import sys
import json
import os
import discord as d
from discord.ext import commands, tasks
from bs4 import BeautifulSoup
import aiohttp
from captcha.image import ImageCaptcha
from discord.ext.commands import has_permissions, MissingPermissions
from youtube_search import YoutubeSearch
import youtube_dl
from random import choice
import math
import aiosqlite
import urllib
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re # Regex for youtube link
import warnings
import requests
from pafy import new
from fast_youtube_search import search_youtube
from Tools.var import prefix, embedcolor, mainprefix, version
from Tools.func import warn, errorlog, is_owner





bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
bot.multiplier = 1



async def initialize():
    await bot.wait_until_ready()
    bot.db = await aiosqlite.connect("expData.db")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS guildData (guild_id int, user_id int, exp int, PRIMARY KEY (guild_id, user_id))")



ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'downloads': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.id = data.get('id')
        self.uploader = data.get('uploader')
        self.uploaderid = data.get('uploader_id')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@bot.event
async def on_ready(): #봇이 준비되었을때 뭐라고하기
    user = len(bot.users)
    server = len(bot.guilds)
    message = ["ㅇ!도움을 쳐보세요!",  str(user) + "유저와 함께해요!", str(server) + "개의 서버에 알파프리베이트가 같이운영해요!"]
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(message[0]))
        message.append(message.pop(0))
        await asyncio.sleep(4)





@bot.command() 
async def 안녕(ctx):
	await ctx.send("그래 안녕!")



@bot.command(aliases=['청소'])
@commands.has_permissions(administrator=True)
async def clear(ctx, l: int = 50):
   c = await ctx.channel.purge(limit=l)
   await ctx.send(f"`{len(c)}` 개의 메세지를 삭제했습니다.", delete_after=3)
   





@bot.command()
async def 밴(ctx, user: discord.User):
	guild = ctx.guild
	mbed = discord.Embed(
		title = '처리 완료',
		description = f"{user}님이 밴을 당하셨어요!"
	)
	if ctx.author.guild_permissions.ban_members:
		await ctx.send(embed=mbed)
		await guild.ban(user=user)

@bot.command()
async def 언밴(ctx, user: discord.User):
	guild = ctx.guild
	mbed = discord.Embed(
		title = '처리완료',
		description = f"{user}님을 언밴 했어요!"
	)
	if ctx.author.guild_permissions.ban_members:
		await ctx.send(embed=mbed)
		await guild.unban(user=user)

@bot.command()
@commands.has_permissions(kick_members=True)
async def 킥(ctx, member:discord.Member):
    await member.kick()
    await ctx.send(f"{member.name}님을 킥했습니다.")

@bot.command(name="뮤트")
@commands.has_permissions(manage_messages=True)
async def mute(ctx , member: discord.Member, *, reason=None):
	guild = ctx.guild
	mutedRole = discord.utils.get(guild.roles, name="Muted")

	if not mutedRole:
		mutedRole = await guild.create_role(name="Muted")

		for channel in guild.channels:
			await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

	await member.add_roles(mutedRole, reason=reason)
	await ctx.send(f"뮤트 {member.mention} 사유: {reason}으로 뮤트를 먹으셨습니다.")
	await member.send(f"뮤트 {member.mention} 사유: {reason}으로 뮤트를 먹으셨습니다.")


@bot.command(name="언뮤트")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
	mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

	
			

	await member.remove_roles(mutedRole)
	await ctx.send(f"언뮤트 {member.mention}님이 언뮤트를 당하셨습니다.")
	await member.send(f"언뮤트 {member.mention}님이  언뮤트를 당하셨습니다.")






 
@bot.command(aliases = ['세이','메세지'])
async def say(ctx,*,message):
    emb=discord.Embed(title="say", description=f"{message}")
    msg=await ctx.channel.send(embed=emb)
    
   

                 
@bot.command()
@commands.has_role("💎AC ▪ MASTER💎")
async def 경품(ctx, mins : int, * , prize: str):
	embed = discord.Embed(title = "상품!", description = f"{prize}", color = ctx.author.color)

	end = datetime.datetime.utcnow() + datetime.timedelta(seconds = mins*60)

	embed.add_field(name = "종료 시간:", value = f"{end} UTC")
	embed.set_footer(text = f"지금부터 {mins}분 후 Emds")

	my_msg = await ctx.send(embed = embed)

	await my_msg.add_reaction("🎉")

@bot.command()
async def 리로드(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded extension: {extension}.")

@bot.command()
async def 언로드(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Unloaded extension: {extension}.")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.command(aliases = ['ㅊㄴㅈㄱ'])
async def 채널제거(ctx, channel: d.TextChannel):
	mbed = d.Embed(
		title = '완료!',
		description = f'{channel}이라는 채널을 삭제했습니다.',
	)
	if ctx.author.guild_permissions.manage_channels:
		await ctx.send(embed=mbed)
		await channel.delete()


@bot.command(aliases = ['ㅊㄴㅅㅅ'])
async def 채널생성(ctx, channelName):
	guild = ctx.guild

	mbed = d.Embed(
		title = '완료!',
		description = "{}이라는 채널을 성공적으로 생성되었습니다.".format(channelName)
	)
	if ctx.author.guild_permissions.manage_channels:
		await guild.create_text_channel(name='{}'.format(channelName))
		await ctx.send(embed=mbed)
		
		
@bot.command(aliases = ['ㄸㄹㅎ'])
async def 따라해(ctx, *, text):
    await ctx.send(text)



@bot.command(pass_context=True)
async def 역할부여(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"{user.name}님한테 **{role.name}**역할을 추가했어요!")

@bot.command(pass_context=True)
async def 역할제거(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f"{user.name}님한테 **{role.name}**역할을 제거했어요!")

@bot.command()
async def 유튜브(ctx):
    embed = discord.Embed(colour=0x95efcc, title=f"알파캡틴유튜브")
    await ctx.send(embed=embed)
    await ctx.send('https://www.youtube.com/user/cho090501')
    
@bot.command()
async def 레일건사기템존(ctx):
    embed=discord.Embed(title='이거 눌러보셈 ㅋㅋㅋㅋㅋㅋㅋ', description = "레일건 사기템존님은?\n잼민티 내고 이상하고 병신임 이거 이욕해도됌 제목눌러보셈", color = 0xff0000, url = "https://www.youtube.com/watch?v=K51gdMm3wWM")
    embed.set_footer(text = "와 니애미 욕은 해도됌 이사람한테는 (?)")
#출처: https://tercomgame.tistory.com/138 [단순한.]
    await ctx.send(embed=embed)


@bot.command()
async def 도움(ctx):
        embed = discord.Embed(title="관리자 명령어", color=0x20ff05)
        embed.add_field(name="ㅇ!도움1", value="관리자 도움말", inline=False) 
        embed.add_field(name="ㅇ!도움2", value="유저 도움말", inline=False)
        embed.add_field(name="ㅇ!도움3", value="게임 도움말", inline=False) 
        await ctx.send(embed=embed)



@bot.command()
async def 도움1(ctx):
        embed = discord.Embed(title="관리자 명령어", color=0x20ff05)
        embed.add_field(name="관리자 명령어", value="`ㅌ밴` `ㅌ언밴` `ㅌ뮤트` `ㅌ언뮤트` `ㅌ청소` `ㅌ역할부여` `ㅌ역할제거`", inline=False) 
        await ctx.send(embed=embed)

@bot.command()
async def 도움2(ctx):
        embed = discord.Embed(title="유저 명령어", color=0x20ff05)
        embed.add_field(name="유저명령어", value="`ㅌ시간` `ㅌ서버정보` `ㅌ유저정보` `ㅌ따라해` `ㅌ한일번역` `한영번역` `ㅌ영한번역` `ㅌ일한번역` `ㅌ날씨` `ㅌ실검` `ㅌ노래순위` `ㅌ검색` `ㅌ롤전적` `ㅌ레식전적`", inline=False) 
        await ctx.send(embed=embed)
   








@bot.command()
async def 입장(msg,*,channel:discord.VoiceChannel = None):
    if channel == None:
        channel = msg.author.voice.channel
    if msg.voice_client is not None:
        await msg.voice_client.move_to(channel)
    else:
        await channel.connect()

@bot.command()
async def 퇴장(msg):
    await msg.voice_client.disconnect()

@bot.command() #재생
async def 재생(ctx, *, url):
    async with ctx.typing():
        player = await YTDLSource.from_url(url)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    e = discord.Embed(title="재생 중!",description=player.title)
    e.set_image(url=f'https://i.ytimg.com/vi/{player.id}/hqdefault.jpg')
    await ctx.send(embed = e)
            
@bot.command()
async def 도움3(ctx):
    embed = discord.Embed(title="게임, 도박 도움말")
    embed.add_field(name="도박", value="`ㅌ출석` `ㅌ포인트` `송금` `ㅌ도박 (올인가능)` `ㅌ새총`", inline=False) 
    embed.set_footer(text="출처:https://github.com/sw08/Finix [제작자 sw08(민트초코)님]")
    await ctx.send(embed=embed)
   
@bot.command()
async def dm(ctx, user_id=None, *, args=None):
    if user_id != None and args != None:
        try:
            target = await bot.fetch_user(user_id)
            await target.send(args)

            await ctx.channel.send("'" + args + "' dm전송이 완료되었습니다.: " + target.name)

        except:
            await ctx.channel.send("지정된 사용자한테 dm을(를)할 수 없습니다.")
        

    else:
        await ctx.channel.send("사용자 ID 및 / 또는 메시지를 제공하지 않았습니다.")
 
@bot.event
async def on_message(message):
    if not message.author.bot:
        cursor = await bot.db.execute("INSERT OR IGNORE INTO guildData (guild_id, user_id, exp) VALUES (?,?,?)", (message.guild.id, message.author.id, 1)) 

        if cursor.rowcount == 0:
            await bot.db.execute("UPDATE guildData SET exp = exp + 1 WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
            cur = await bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
            data = await cur.fetchone()
            exp = data[0]
            lvl = math.sqrt(exp) / bot.multiplier
        
            if lvl.is_integer():
                await message.channel.send(f"{message.author.mention} 축하합니다. 레벨업 하셨어요! \n`ㅇ!rank`로 자신에 정보를 확인해보세요!\n현재레벨: {int(lvl)}.")

        await bot.db.commit()

    await bot.process_commands(message)





@bot.command()
async def 시간(ctx):
    await ctx.send(embed=discord.Embed(title="현재시간", timestamp=datetime.datetime.utcnow()))



    



@bot.command()
async def play(ctx, *, search):
    m = await ctx.send("`🎵 로딩중...`")
    results = search_youtube([search])[0]
    try:
        video = new(f"https://www.youtube.com/watch?v={results['id']}")
    except OSError:
        return await m.edit(content="노래를 검색하던 중 오류가 발생했어요. 잠시 후에 다시 시도해주세요.")
    channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        voice = await channel.connect()
    else:
        voice = ctx.voice_client
    music = discord.FFmpegPCMAudio(executable='ffmpeg', source=video.getbestaudio().url, 
                                        before_options=" -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 0 -nostdin",
                                        options="-vn -loglevel quiet -hide_banner -nostats")
    voice.play(music)
    await m.edit(content='노래 재생 시작')


@bot.command(name="검색")
async def s(ctx, *, search_query):
    temp = 0
    url_base = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query="
    url = url_base + urllib.parse.quote(search_query)
    title = ["", "", "", ""]
    link = ["", "", "", ""]
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
    result = soup.find_all('a', "api_txt_lines total_tit") #수정됨
    embed = discord.Embed(title="검색 결과", description=" ", color=0xf3bb76)
    for n in result:
        if temp == 4:
            break
        title[temp] = n.text #수정됨
        link[temp] = n.get("href")
        embed.add_field(name=title[temp], value=link[temp], inline=False)
        temp+=1
    embed.set_footer(text="네이버 블로그만 검색됩니다.")
    await ctx.send(embed=embed)




@bot.command()
async def 뽑기(ctx):
        await ctx.trigger_typing()
        randomNum = random.randrange(1, 3)
        if randomNum == 1:
            await ctx.send('당첨')
        if randomNum == 2:
            await ctx.send('꽝')








bot.loop.create_task(initialize())
bot.run('봇토큰은 비밀')
bot.remove_command("help")
asyncio.run(bot.db.close())
