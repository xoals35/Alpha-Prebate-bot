import discord, datetime, time
from discord.ext import commands
import asyncio
from urllib import request
import time
import random
import pickle
import warnings
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
import re
import asyncio
import discord 
import bs4
import urllib
import re
import requests
from discord.ext import commands
import os
import time
import random
import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib import parse
import json
from urllib import request
import bs4
import urllib
import re
import requests
import lxml
from discord.ext import commands
import os
import time
import random
import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib import parse
import json
from urllib import request
import platform
import psutil





embedcolor = 0xffff33
embederrorcolor = 0xff0000
start_time = time.time()

class Test(commands.Cog, name="관리자"):
    def __init__(self, bot):
        self.bot = bot

    
        

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command(pass_context=True)
    async def 업타임(self, ctx):
            current_time = time.time()
            difference = int(round(current_time - start_time))
            text = str(datetime.timedelta(seconds=difference))
            embed = discord.Embed(colour=0xc8dc6c)
            embed.add_field(name="업타임", value=text)
            embed.set_footer(text="<알파프리베이트>")
            try:
                await ctx.send(embed=embed)
            except discord.HTTPException:
                await ctx.send("현재 봇작동시간: " + text)

    @commands.command()
    async def 새총(self, ctx):
        await ctx.trigger_typing()

        randomNum = random.randrange(1, 4)
        if randomNum == 1:
            embed = discord.Embed(title="새총으로 새를 잡았어요!", description="정말 잘했어요!")
            await ctx.send(embed=embed)
        if randomNum == 2:
            embed = discord.Embed(title="으악!!", description="새총을 쏘았는데 늑대가 왔어요 얼른 도망쳐요!")
            await ctx.send(embed=embed)
        if randomNum == 3:
            embed = discord.Embed(title="새총을 쏘았어요!", description="새총을 쏘았더니 경찰이었어요 도망쳐요!")
            await ctx.send(embed=embed)

    @commands.command()
    async def covid(self, ctx):
            # 보건복지부 코로나 바이러스 정보사이트"
            covidSite = "http://ncov.mohw.go.kr/index.jsp"
            covidNotice = "http://ncov.mohw.go.kr"
            html = urlopen(covidSite)
            bs = BeautifulSoup(html, 'html.parser')
            latestupdateTime = bs.find('span', {'class': "livedate"}).text.split(',')[0][1:].split('.')
            statisticalNumbers = bs.findAll('span', {'class': 'num'})
            beforedayNumbers = bs.findAll('span', {'class': 'before'})

            #주요 브리핑 및 뉴스링크
            briefTasks = []
            mainbrief = bs.findAll('a',{'href' : re.compile('\/tcmBoardView\.do\?contSeq=[0-9]*')})
            for brf in mainbrief:
                container = []
                container.append(brf.text)
                container.append(covidNotice + brf['href'])
                briefTasks.append(container)
        # 통계수치
            statNum = []
        # 전일대비 수치
            beforeNum = []
            for num in range(7):
                statNum.append(statisticalNumbers[num].text)
            for num in range(4):
                beforeNum.append(beforedayNumbers[num].text.split('(')[-1].split(')')[0])

            totalPeopletoInt = statNum[0].split(')')[-1].split(',')
            tpInt = ''.join(totalPeopletoInt)
            embed = discord.Embed(title="Covid-19 바이러스 코리아 현황", description="",color=0x5CD1E5)
            embed.add_field(name="자료 출처 : 보건 복지부", value="http://ncov.mohw.go.kr/index.jsp", inline=False)
            embed.add_field(name="최신 데이터 재생 시간",value="해당 자료는 " + latestupdateTime[0] + "월 " + latestupdateTime[1] + "일 "+latestupdateTime[2] +" 자료입니다.", inline=False)
            embed.add_field(name="확진환자(누적)", value=statNum[0].split(')')[-1]+"("+beforeNum[0]+")",inline=True)
            embed.add_field(name="완치환자(격리해제)", value=statNum[1] + "(" + beforeNum[1] + ")", inline=True)
            embed.add_field(name="치료중(격리 중)", value=statNum[2] + "(" + beforeNum[2] + ")", inline=True)
            embed.add_field(name="사망", value=statNum[3] + "(" + beforeNum[3] + ")", inline=True)
            embed.add_field(name="누적확진률", value=statNum[6], inline=True)
            embed.add_field(name="- 최신 브리핑 1 : " + briefTasks[0][0],value="Link : " + briefTasks[0][1],inline=False)
            embed.add_field(name="- 최신 브리핑 2 : " + briefTasks[1][0], value="Link : " + briefTasks[1][1], inline=False)
            embed.add_field(name="Covid-19 확진 현황봇", value= "개발자 | hacking-Defender#4202 | 공식 커뮤니티 서버초대 초드 | http://asq.kr/djCAi4inQNMaUc")
            embed.set_thumbnail(url="https://wikis.krsocsci.org/images/7/79/%EB%8C%80%ED%95%9C%EC%99%95%EA%B5%AD_%ED%83%9C%EA%B7%B9%EA%B8%B0.jpg")
            await ctx.send(embed=embed)

    @commands.command(name='투표')
    async def Vote(self, ctx, *, vote: str = None):
        if vote == None:
            return await ctx.reply(embed=discord.Embed(title="명령어 오류", description="올바른 명령어는 '/투표 [제목]/항목1/항목2 ... 이에요", color=0xff0000))
        vote = vote.split('/')
        await ctx.reply(f'투표 - {vote[0]}')
        for i in range(1, len(vote)):
            a = await ctx.send(f'```{vote[i]}```')
            await a.add_reaction('👍')
            await a.add_reaction('👎')



    @commands.command()
    async def 계산(self,ctx, act, num1:int, num2:int):
        if act == ("더하기"):
            calcResult = float(num1)+float(num2)
            await ctx.send(str(calcResult))
        elif act == ("빼기"):
            calcResult = float(num1)-float(num2)
            await ctx.send(str(calcResult))
        elif act == ("곱하기"):
            calcResult = float(num1)*float(num2)
            await ctx.send(str(calcResult))
        elif act == ("나누기"):
            calcResult = float(num1)/float(num2)
            await ctx.send(str(calcResult))
        else:
            await ctx.send("더하기 빼기 곱하기 나누기 로 해주세요.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            embed=discord.Embed(title=f'환영합니다!',description=f'{member.mention}님이  {member.guild}에 들어오셨습니다.  \n현재 서버 인원수: {str(len(member.guild.members))}명',color=embedcolor)
            embed.set_footer(text="환영메시지를 받고싶지 않으시면 봇이 이 채널을 못보게 해주세요")
            embed.set_thumbnail(url=member.avatar_url)
            await member.guild.system_channel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            embed=discord.Embed(title=f'안녕히 가세요',description=f'{member.mention}님이  나가셨습니다.  \n현재 서버 인원수: {str(len(member.guild.members))}명',color=embederrorcolor)
            embed.set_footer(text="퇴장메시지를 받고싶지 않으시면 봇이 이 채널을 못보게 해주세요")
            embed.set_thumbnail(url=member.avatar_url)
            await member.guild.system_channel.send(embed=embed)
        except:
            pass

    @commands.command(name="핑", help="핑을 보여줌")
    async def ping(self, ctx):
        pings = round(self.bot.latency*1000)
        if pings < 100:
            pinglevel = '🔵 매우좋음'
            color=embedcolor
        elif pings < 300: 
            pinglevel = '🟢 양호함'
            color=embedcolor
        elif pings < 400: 
            pinglevel = '🟡 보통'
            color=embedcolor
        elif pings < 6000: 
            pinglevel = '🔴 나쁨'
            color=embederrorcolor
        else: 
            pinglevel = '⚪ 매우나쁨'
            color=embederrorcolor
        embed = discord.Embed(title='핑', description=f'{pings} ms\n{pinglevel}', color=color)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 3, commands.BucketType.user) 
    @commands.command(name="봇정보", help="봇정보 알려줌")
    async def infinitybot_info(self, ctx):
        embed1 = discord.Embed(title="봇정보를 불러오는중입니다....", description="이 작업은 10초정도 걸립니다", color=embedcolor)
        info = await ctx.send(embed=embed1)
        date = datetime.datetime.utcfromtimestamp(((int(self.bot.user.id) >> 22) + 1420070400000) / 1000)
        embed = discord.Embed(title=f'{self.bot.user.name}봇 정보', color=embedcolor)
        embed.add_field(name="이름", value=self.bot.user, inline=False)
        embed.add_field(name="별명", value=self.bot.user.display_name, inline=True)
        embed.add_field(name="가입일", value=str(date.year) + "년" + str(date.month) + "월" + str(date.day) + "일", inline=False)
        embed.add_field(name="아이디", value=self.bot.user.id, inline=False)
        embed.add_field(name="운영체제", value=platform.system())
        embed.add_field(name="운영체제 버젼", value=platform.version())
        embed.add_field(name="프로세스 아키텍쳐", value=platform.machine())
        embed.add_field(name="램 크기", value=str(round(psutil.virtual_memory().total / (1024.0 **3)))+"(GB)", inline=False)
        embed.add_field(name="서버 수", value=len(self.bot.guilds))
        embed.add_field(name="유저 수", value=len(self.bot.users))
        embed.add_field(name="개발자", value="리펙스#1036")
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await info.edit(embed=embed)



    

   

def setup(bot):
    bot.add_cog(Test(bot))