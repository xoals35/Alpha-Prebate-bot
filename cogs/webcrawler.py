import discord
import datetime
import warnings
import re
import requests
import bs4
import urllib
import requests as rq
from discord.ext import commands
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from urllib.parse import quote
from urllib.request import HTTPError
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

embedcolor = 0xffff33
embederrorcolor = 0xff0000
colour = discord.Colour.blue()

opggsummonersearch = 'https://www.op.gg/summoner/userName='

tierScore = {
        'default': 0,
        'iron': 1,
        'bronze': 2,
        'silver': 3,
        'gold': 4,
        'platinum': 5,
        'diamond': 6,
        'master': 7,
        'grandmaster': 8,
        'challenger': 9
    }

r6URL = "https://r6stats.com"
playerSite = 'https://www.r6stats.com/search/'


def deleteTags(htmls):
    for a in range(len(htmls)):
        htmls[a] = re.sub('<.+?>', '', str(htmls[a]), 0).strip()
    return htmls


def tierCompare(solorank, flexrank):
    if tierScore[solorank] > tierScore[flexrank]:
        return 0
    elif tierScore[solorank] < tierScore[flexrank]:
        return 1
    else:
        return 2

warnings.filterwarnings(action='ignore')


class 크롤링(commands.Cog):
    """웹크롤링을 활용한 기능들을 보여줍니다"""

    def __init__(self, client):
        self.client = client

    @commands.command(name="날씨", pass_context=True)
    async def weather(self, ctx, location):
        """날씨를 알려줍니다"""
        embed = discord.Embed(
            title="날씨",
            colour=colour
        )
        Finallocation = location + '날씨'
        LocationInfo = ""
        NowTemp = ""
        CheckDust = []
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + Finallocation
        hdr = {'User-Agent': (
            'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/78.0.3904.70 safari/537.36')}
        req = requests.get(url, headers=hdr)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        # 오류 체크
        ErrorCheck = soup.find('span', {'class': 'btn_select'})

        if 'None' in str(ErrorCheck):
            await ctx.send('검색 오류발생')
        else:
            # 지역 정보
            for i in soup.select('span[class=btn_select]'):
                LocationInfo = i.text

            NowTemp = soup.find('span', {'class': 'todaytemp'}).text + soup.find('span', {'class': 'tempmark'}).text[2:]

            WeatherCast = soup.find('p', {'class': 'cast_txt'}).text

            TodayMorningTemp = soup.find('span', {'class': 'min'}).text
            TodayAfternoonTemp = soup.find('span', {'class': 'max'}).text
            TodayFeelTemp = soup.find('span', {'class': 'sensible'}).text[5:]

            TodayUV = soup.find('span', {'class': 'indicator'}).text[4:-2] + " " + soup.find('span', {
                'class': 'indicator'}).text[-2:]

            CheckDust1 = soup.find('div', {'class': 'sub_info'})
            CheckDust2 = CheckDust1.find('div', {'class': 'detail_box'})
            for i in CheckDust2.select('dd'):
                CheckDust.append(i.text)
            FineDust = CheckDust[0][:-2] + " " + CheckDust[0][-2:]
            UltraFineDust = CheckDust[1][:-2] + " " + CheckDust[1][-2:]
            Ozon = CheckDust[2][:-2] + " " + CheckDust[2][-2:]

            embed.add_field(name="지역", value=f"{LocationInfo}")
            embed.add_field(name="현재온도", value=f"{NowTemp}", inline=False)
            embed.add_field(name="체감온도", value=f"{TodayFeelTemp}", inline=False)
            embed.add_field(name="정보", value=f"{WeatherCast}", inline=False)
            embed.add_field(name="자외선", value=f"{TodayUV}", inline=False)
            embed.add_field(name="최저온도/최고온도", value=f"{TodayMorningTemp}/{TodayAfternoonTemp}", inline=False)
            embed.add_field(name="미세먼지", value=f"{FineDust}", inline=False)
            embed.add_field(name="초미세먼지", value=f"{UltraFineDust}", inline=False)
            embed.add_field(name="오존 지수", value=f"{Ozon}", inline=False)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)


    @commands.command(name="인벤", pass_context=True)
    async def inven(self, ctx):
        """인벤의 주요뉴스를 보여줍니다"""
        embed = discord.Embed(
            title="인벤 주요뉴스",
            colour=colour
        )
        targetSite = 'http://www.inven.co.kr/webzine/news/?hotnews=1'

        header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        melonrqRetry = rq.get(targetSite, headers=header)
        melonht = melonrqRetry.text
        melonsp = bs(melonht, 'html.parser')
        artists = melonsp.findAll('span', {'class': 'title'})
        titles = melonsp.findAll('span', {'class': 'summary'})
        for i in range(len(titles)):
            artist = artists[i].text.strip()
            title = titles[i].text.strip()
            embed.add_field(name="{0:3d}".format(i + 1), value='제목:{0} - 내용:{1}'.format(artist, title), inline=False)
            embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(name="노래순위", pass_context=True)
    async def music(self, ctx):
        """멜론차트를 모여줍니다."""
        embed = discord.Embed(
            title="노래순위",
            description="노래순위입니다.",
            colour=colour
        )
        targetSite = 'https://www.melon.com/chart/index.htm'

        header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        melonrqRetry = rq.get(targetSite, headers=header)
        melonht = melonrqRetry.text
        melonsp = bs(melonht, 'html.parser')
        artists = melonsp.findAll('span', {'class': 'checkEllipsis'})
        titles = melonsp.findAll('div', {'class': 'ellipsis rank01'})
        for i in range(len(titles)):
            artist = artists[i].text.strip()
            title = titles[i].text.strip()
            embed.add_field(name="{0:3d}위".format(i + 1), value='{0} - {1}'.format(artist, title), inline=False)
            embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(name="실검", aliases = ['실시간검색어'], help="실시간 검색어를 보여줍니다.")
    async def search(self, ctx):
        url="https://datalab.naver.com/keyword/realtimeList.naver?where=main"
        req=urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36 '})
        html=urllib.request.urlopen(req)
        bs=bs4.BeautifulSoup(html, "lxml")
        Time=bs.find('a', {'class': 'time_box _time_trigger'}).find('span', {'class': 'time_txt _title_hms'}).text.strip()
        list_group=bs.find('div', {'class': 'list_group'}).find_all('ul', {'class': 'ranking_list'})
        embed=discord.Embed(description='실시간 검색어', color=embedcolor)
        embed.set_footer(text=f'{Time} 기준')
        rank = 0
        for ranking_list in list_group:
            ranking_item=ranking_list.find_all('li')
            for item in ranking_item:
                rank += 1
                item_title=item.find('span', {'class': 'item_title'}).text.strip()
                ranking_url="https://search.naver.com/search.naver?ie=utf8&query="+item_title.replace(' ', '+')
                embed.add_field(name=f'{rank}위', value=f'[{item_title}]({ranking_url})', inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="롤전적", pass_context=True)
    async def lol(self, ctx, *, playerNickname):
        """롤전적을 보여줍니다."""
        checkURLBool = urlopen(opggsummonersearch + quote(playerNickname))
        bs = BeautifulSoup(checkURLBool, 'html.parser')

        # 자유랭크 언랭은 뒤에 '?image=q_auto&v=1'표현이없다
        RankMedal = bs.findAll('img', {
            'src': re.compile('\/\/[a-z]*\-[A-Za-z]*\.[A-Za-z]*\.[A-Za-z]*\/[A-Za-z]*\/[A-Za-z]*\/[a-z0-9_]*\.png')})
        # index 0 : Solo Rank
        # index 1 : Flexible 5v5 rank

        # for mostUsedChampion
        mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
        mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})

        # 솔랭, 자랭 둘다 배치가 안되어있는경우 -> 사용된 챔피언 자체가 없다. 즉 모스트 챔피언 메뉴를 넣을 필요가 없다.

        if len(playerNickname) == 1:
            embed = discord.Embed(title="소환사 이름이 입력되지 않았습니다!", description="", color=colour)
            embed.add_field(name="Summoner name not entered",
                            value="To use command !롤전적 : !롤전적 (Summoner Nickname)", inline=False)
            await ctx.send("Error : Incorrect command usage ", embed=embed)

        elif len(deleteTags(bs.findAll('h2', {'class': 'Title'}))) != 0:
            embed = discord.Embed(title="존재하지 않는 소환사", description="", color=colour)
            embed.add_field(name="해당 닉네임의 소환사가 존재하지 않습니다.", value="소환사 이름을 확인해주세요", inline=False)
            await ctx.send("Error : Non existing Summoner ", embed=embed)
        else:
            try:
                # Scrape Summoner's Rank information
                # [Solorank,Solorank Tier]
                solorank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {'class': {'RankType', 'TierRank'}}))
                # [Solorank LeaguePoint, Solorank W, Solorank L, Solorank Winratio]
                solorank_Point_and_winratio = deleteTags(
                    bs.findAll('span', {'class': {'LeaguePoints', 'wins', 'losses', 'winratio'}}))
                # [Flex 5:5 Rank,Flexrank Tier,Flextier leaguepoint + W/L,Flextier win ratio]
                flexrank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {
                    'class': {'sub-tier__rank-type', 'sub-tier__rank-tier', 'sub-tier__league-point',
                              'sub-tier__gray-text'}}))
                # ['Flextier W/L]
                flexrank_Point_and_winratio = deleteTags(bs.findAll('span', {'class': {'sub-tier__gray-text'}}))

                # embed.set_imag()는 하나만 들어갈수 있다.

                # 솔랭, 자랭 둘다 배치 안되어있는 경우 -> 모스트 챔피언 출력 X
                if len(solorank_Point_and_winratio) == 0 and len(flexrank_Point_and_winratio) == 0:
                    embed = discord.Embed(title="소환사 전적검색", description="", color=colour)
                    embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,
                                    inline=False)
                    embed.add_field(name="Ranked Solo : Unranked", value="Unranked", inline=False)
                    embed.add_field(name="Flex 5:5 Rank : Unranked", value="Unranked", inline=False)
                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    await ctx.send("소환사 " + playerNickname + "님의 전적", embed=embed)

                # 솔로랭크 기록이 없는경우
                elif len(solorank_Point_and_winratio) == 0:

                    # most Used Champion Information : Champion Name, KDA, Win Rate
                    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                    mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    FlexRankTier = flexrank_Types_and_Tier_Info[0] + ' : ' + flexrank_Types_and_Tier_Info[1]
                    FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + flexrank_Types_and_Tier_Info[-1]
                    embed = discord.Embed(title="소환사 전적검색", description="", color=colour)
                    embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,
                                    inline=False)
                    embed.add_field(name="Ranked Solo : Unranked", value="Unranked", inline=False)
                    embed.add_field(name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
                    embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                    value="KDA : " + mostUsedChampionKDA + " / " + " WinRate : " + mostUsedChampionWinRate,
                                    inline=False)
                    embed.set_thumbnail(url='https:' + RankMedal[1]['src'])
                    await ctx.send("소환사 " + playerNickname + "님의 전적", embed=embed)

                # 자유랭크 기록이 없는경우
                elif len(flexrank_Point_and_winratio) == 0:

                    # most Used Champion Information : Champion Name, KDA, Win Rate
                    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                    mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    SoloRankTier = solorank_Types_and_Tier_Info[0] + ' : ' + solorank_Types_and_Tier_Info[1]
                    SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[
                        1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
                    embed = discord.Embed(title="소환사 전적검색", description="", color=colour)
                    embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,
                                    inline=False)
                    embed.add_field(name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
                    embed.add_field(name="Flex 5:5 Rank : Unranked", value="Unranked", inline=False)
                    embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                    value="KDA : " + mostUsedChampionKDA + " / " + "WinRate : " + mostUsedChampionWinRate,
                                    inline=False)
                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    await ctx.send("소환사 " + playerNickname + "님의 전적", embed=embed)
                # 두가지 유형의 랭크 모두 완료된사람
                else:
                    # 더 높은 티어를 thumbnail에 안착
                    solorankmedal = RankMedal[0]['src'].split('/')[-1].split('?')[0].split('.')[0].split('_')
                    flexrankmedal = RankMedal[1]['src'].split('/')[-1].split('?')[0].split('.')[0].split('_')

                    # Make State
                    SoloRankTier = solorank_Types_and_Tier_Info[0] + ' : ' + solorank_Types_and_Tier_Info[1]
                    SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[
                        1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
                    FlexRankTier = flexrank_Types_and_Tier_Info[0] + ' : ' + flexrank_Types_and_Tier_Info[1]
                    FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + flexrank_Types_and_Tier_Info[-1]

                    # most Used Champion Information : Champion Name, KDA, Win Rate
                    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                    mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    cmpTier = tierCompare(solorankmedal[0], flexrankmedal[0])
                    embed = discord.Embed(title="소환사 전적검색", description="", color=colour)
                    embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,
                                    inline=False)
                    embed.add_field(name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
                    embed.add_field(name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
                    embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                    value="KDA : " + mostUsedChampionKDA + " / " + " WinRate : " + mostUsedChampionWinRate,
                                    inline=False)
                    if cmpTier == 0:
                        embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    elif cmpTier == 1:
                        embed.set_thumbnail(url='https:' + RankMedal[1]['src'])
                    else:
                        if solorankmedal[1] > flexrankmedal[1]:
                            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                        elif solorankmedal[1] < flexrankmedal[1]:
                            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                        else:
                            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    await ctx.send("소환사 " + playerNickname + "님의 전적", embed=embed)
            except HTTPError as e:
                embed = discord.Embed(title="소환사 전적검색 실패", description="", color=colour)
                embed.add_field(name="", value="올바르지 않은 소환사 이름입니다. 다시 확인해주세요!", inline=False)
                await ctx.send("Wrong Summoner Nickname")

            except UnicodeEncodeError as e:
                embed = discord.Embed(title="소환사 전적검색 실패", description="", color=colour)
                embed.add_field(name="???", value="올바르지 않은 소환사 이름입니다. 다시 확인해주세요!", inline=False)
                await ctx.send("Wrong Summoner Nickname", embed=embed)

    @commands.command(name="영화순위", pass_context=True)
    async def movie(self, ctx):
        """영화를 1~20순위로 나눈 영화순위를 보여줍니다."""
        # http://ticket2.movie.daum.net/movie/movieranklist.aspx
        i1 = 0  # 랭킹 string값
        embed = discord.Embed(
            title="영화순위",
            description="영화순위입니다.",
            colour=colour
        )
        hdr = {'User-Agent': 'Mozilla/5.0'}
        url = 'http://ticket2.movie.daum.net/movie/movieranklist.aspx'
        req = Request(url, headers=hdr)
        html = urllib.request.urlopen(req)
        bsObj = bs4.BeautifulSoup(html, "html.parser")
        moviechartBase = bsObj.find('div', {'class': 'main_detail'})
        moviechart1 = moviechartBase.find('ul', {'class': 'list_boxthumb'})
        moviechart2 = moviechart1.find_all('li')
        for i in range(0, 20):
            i1 = i1 + 1
            stri1 = str(i1)  # i1은 영화랭킹을 나타내는데 사용됩니다
            moviechartLi1 = moviechart2[i]  # ------------------------- 1등랭킹 영화---------------------------
            moviechartLi1Div = moviechartLi1.find('div', {'class': 'desc_boxthumb'})  # 영화박스 나타내는 Div
            moviechartLi1MovieName1 = moviechartLi1Div.find('strong', {'class': 'tit_join'})
            moviechartLi1MovieName = moviechartLi1MovieName1.text.strip()  # 영화 제목
            moviechartLi1Ratting1 = moviechartLi1Div.find('div', {'class': 'raking_grade'})
            moviechartLi1Ratting2 = moviechartLi1Ratting1.find('em', {'class': 'emph_grade'})
            moviechartLi1Ratting = moviechartLi1Ratting2.text.strip()  # 영화 평점
            moviechartLi1openDay1 = moviechartLi1Div.find('dl', {'class': 'list_state'})
            moviechartLi1openDay2 = moviechartLi1openDay1.find_all('dd')  # 개봉날짜, 예매율 두개포함한 dd임
            moviechartLi1openDay3 = moviechartLi1openDay2[0]
            moviechartLi1Yerating1 = moviechartLi1openDay2[1]
            moviechartLi1openDay = moviechartLi1openDay3.text.strip()  # 개봉날짜
            moviechartLi1Yerating = moviechartLi1Yerating1.text.strip()  # 예매율 ,랭킹변동
            embed.add_field(name='---------------랭킹' + stri1 + '위---------------',
                            value='\n영화제목 : ' + moviechartLi1MovieName + '\n영화평점 : ' + moviechartLi1Ratting + '점' + '\n개봉날짜 : ' + moviechartLi1openDay + '\n예매율,랭킹변동 : ' + moviechartLi1Yerating,
                            inline=False)  # 영화랭킹
            embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(name="코로나", help="국내 코로나 상황")
    async def corona(self, ctx):
        url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, "html.parser")
        datecr = soup.find('span', {'class': 't_date'})
        totalcovid = soup.select('dd.ca_value')[0].text
        todaytotalcovid = soup.select('p.inner_value')[0].text
        todaydomecovid = soup.select('p.inner_value')[1].text
        todayforecovid = soup.select('p.inner_value')[2].text
        totalca = soup.select('dd.ca_value')[2].text
        todayca = soup.select('span.txt_ntc')[0].text
        totalcaing = soup.select('dd.ca_value')[4].text
        todaycaing = soup.select('span.txt_ntc')[1].text
        totaldead = soup.select('dd.ca_value')[6].text
        todaydead = soup.select('span.txt_ntc')[2].text
        embed = discord.Embed(title='코로나19 국내 발생현황', color=embedcolor, url='http://ncov.mohw.go.kr/')
        embed.add_field(name='확진자', value=f'{totalcovid}({todaytotalcovid})명\n국내발생: {todaydomecovid} 명\n해외유입: {todayforecovid} 명', inline=False)
        embed.add_field(name='격리중', value=f'{totalcaing}({todaycaing}) 명', inline=False)
        embed.add_field(name='격리해제', value=f'{totalca}({todayca}) 명', inline=False)
        embed.add_field(name='사망자', value=f'{totaldead}({todaydead}) 명', inline=False)
        embed.set_footer(text=datecr.string)
        await ctx.send(embed=embed)



    @commands.command(name="레식전적")
    async def rss(self, ctx, name):
        """레식 전적을 보여줍니다"""
        playerNickname = name
        html = requests.get(playerSite + playerNickname + '/pc/').text
        bs = BeautifulSoup(html, 'html.parser')

        # 한번에 검색 안되는 경우에는 해당 반환 리스트의 길이 존재. -> bs.find('div',{'class' : 'results'}

        if bs.find('div', {'class': 'results'}) == None:
            # Get latest season's Rank information
            latestSeason = bs.find('div', {'class': re.compile('season\-rank operation\_[A-Za-z_]*')})

            # if player nickname not entered
            if len(name) == 1:
                embed = discord.Embed(title="플레이어 이름이 입력되지 않았습니다", description="", color=0x5CD1E5)
                embed.add_field(name="Error : Player name not entered" + playerNickname,
                                value="To use command : !레식전적 (nickname)")
                await ctx.send("Error : Player name not entered ", embed=embed)

            # search if it's empty page
            elif latestSeason == None:
                embed = discord.Embed(title="해당 이름을 가진 플레이어가 존재하지않습니다.", description="", color=0x5CD1E5)
                embed.add_field(name="Error : Can't find player name " + playerNickname,
                                value="Please check player's nickname")
                await ctx.send("Error : Can't find player name " + playerNickname, embed=embed)

            # Command entered well
            else:
                # r6stats profile image
                r6Profile = bs.find('div', {'class': 'main-logo'}).img['src']

                # player level
                playerLevel = bs.find('span', {'class': 'quick-info__value'}).text.strip()

                RankStats = bs.find('div', {'class': 'card stat-card block__ranked horizontal'}).findAll('span', {
                    'class': 'stat-count'})
                # Get text from <span> values
                for info in range(len(RankStats)):
                    RankStats[info] = RankStats[info].text.strip()
                # value of variable RankStats : [Timeplayed, Match Played,kills per matchm, kills,death, KDA Rate,Wins,Losses,W/L Rate]

                # latest season tier medal
                lastestSeasonRankMedalLocation = latestSeason.div.img['src']
                # latest Season tier
                lastestSeasonRankTier = latestSeason.div.img['alt']
                # latest season operation name
                OperationName = latestSeason.find('div', {'class': 'meta-wrapper'}).find('div', {
                    'class': 'operation-title'}).text.strip()
                # latest season Ranking
                latestSeasonRanking = latestSeason.find('div', {'class': 'rankings-wrapper'}).find('span', {
                    'class': 'ranking'})

                # if player not ranked, span has class not ranked if ranked span get class ranking
                if latestSeasonRanking == None:
                    latestSeasonRanking = bs.find('span', {'class': 'not-ranked'}).text.upper()
                else:
                    latestSeasonRanking = latestSeasonRanking.text

                # Add player's MMR Rank MMR Information
                playerInfoMenus = bs.find('a', {'class': 'player-tabs__season_stats'})['href']
                mmrMenu = r6URL + playerInfoMenus
                html = requests.get(mmrMenu).text
                bs = BeautifulSoup(html, 'html.parser')

                # recent season rank box
                # Rank show in purpose : America - Europe - Asia. This code only support Asia server's MMR
                getElements = bs.find('div', {
                    'class': 'card__content'})  # first elements with class 'card__contet is latest season content box

                for ckAsia in getElements.findAll('div', {'class': 'season-stat--region'}):
                    checkRegion = ckAsia.find('div', {'class': 'season-stat--region-title'}).text
                    if checkRegion == "Asia":
                        getElements = ckAsia
                        break
                    else:
                        pass

                # Player's Tier Information
                latestSeasonTier = getElements.find('img')['alt']
                # MMR Datas Info -> [Win,Losses,Abandon,Max,W/L,MMR]
                mmrDatas = []
                for dt in getElements.findAll('span', {'class': 'season-stat--region-stats__stat'}):
                    mmrDatas.append(dt.text)

                embed = discord.Embed(title="r6stats에서 Rainbow Six Siege 플레이어 검색", description="",
                                      color=0x5CD1E5)
                embed.add_field(name="r6stats에서 플레이어 검색", value=playerSite + playerNickname + '/pc/',
                                inline=False)
                embed.add_field(name="플레이어의 기본 정보",
                                value="Ranking : #" + latestSeasonRanking + " | " + "Level : " + playerLevel,
                                inline=False)
                embed.add_field(name="최신 시즌 정보 | Operation : " + OperationName,
                                value=
                                "Tier(Asia) : " + latestSeasonTier + " | W/L : " + mmrDatas[0] + "/" + mmrDatas[
                                    1] + " | " + "MMR(Asia) : " + mmrDatas[-1],
                                inline=False)

                embed.add_field(name="총플레이시간", value=RankStats[0], inline=True)
                embed.add_field(name="경기한수", value=RankStats[1], inline=True)
                embed.add_field(name="경기당 처치", value=RankStats[2], inline=True)
                embed.add_field(name="총킬", value=RankStats[3], inline=True)
                embed.add_field(name="총사망", value=RankStats[4], inline=True)
                embed.add_field(name="K/D 비율", value=RankStats[5], inline=True)
                embed.add_field(name="우승", value=RankStats[6], inline=True)
                embed.add_field(name="페베", value=RankStats[7], inline=True)
                embed.add_field(name="W/L 비율", value=RankStats[8], inline=True)
                embed.set_thumbnail(url=r6URL + r6Profile)
                await ctx.send("Player " + playerNickname + "'s stats search", embed=embed)
        else:
            searchLink = bs.find('a', {'class': 'result'})
            if searchLink == None:
                embed = discord.Embed(title="해당 이름을 가진 플레이어가 존재하지않습니다.", description="", color=0x5CD1E5)
                embed.add_field(name="Error : Can't find player name " + playerNickname,
                                value="Please check player's nickname")
                await ctx.send("Error : Can't find player name " + playerNickname, embed=embed)
            else:
                searchLink = r6URL + searchLink['href']
                html = requests.get(searchLink).text
                bs = BeautifulSoup(html, 'html.parser')
                # Get latest season's Rank information
                latestSeason = bs.findAll('div', {'class': re.compile('season\-rank operation\_[A-Za-z_]*')})[0]

                # if player nickname not entered
                if len(name) == 1:
                    embed = discord.Embed(title="플레이어 이름이 입력되지 않았습니다", description="", color=0x5CD1E5)
                    embed.add_field(name="Error : Player name not entered" + playerNickname,
                                    value="To use command : !레식전적 (nickname)")
                    await ctx.send("Error : Player name not entered ", embed=embed)

                # search if it's empty page
                elif latestSeason == None:
                    embed = discord.Embed(title="해당 이름을 가진 플레이어가 존재하지않습니다.", description="", color=0x5CD1E5)
                    embed.add_field(name="Error : Can't find player name " + playerNickname,
                                    value="Please check player's nickname")
                    await ctx.send("Error : Can't find player name " + playerNickname, embed=embed)

                # Command entered well
                else:

                    # r6stats profile image
                    r6Profile = bs.find('div', {'class': 'main-logo'}).img['src']

                    # player level
                    playerLevel = bs.find('span', {'class': 'quick-info__value'}).text.strip()

                    RankStats = bs.find('div', {'class': 'card stat-card block__ranked horizontal'}).findAll('span', {
                        'class': 'stat-count'})
                    # Get text from <span> values
                    for info in range(len(RankStats)):
                        RankStats[info] = RankStats[info].text.strip()
                    # value of variable RankStats : [Timeplayed, Match Played,kills per matchm, kills,death, KDA Rate,Wins,Losses,W/L Rate]

                    # latest season tier medal
                    lastestSeasonRankMedalLocation = latestSeason.div.img['src']
                    # latest Season tier
                    lastestSeasonRankTier = latestSeason.div.img['alt']
                    # latest season operation name
                    OperationName = latestSeason.find('div', {'class': 'meta-wrapper'}).find('div', {
                        'class': 'operation-title'}).text.strip()
                    # latest season Ranking
                    latestSeasonRanking = latestSeason.find('div', {'class': 'rankings-wrapper'}).find('span', {
                        'class': 'ranking'})

                    # if player not ranked, span has class not ranked if ranked span get class ranking
                    if latestSeasonRanking == None:
                        latestSeasonRanking = bs.find('span', {'class': 'not-ranked'}).text.upper()
                    else:
                        latestSeasonRanking = latestSeasonRanking.text

                    # Add player's MMR Rank MMR Information
                    playerInfoMenus = bs.find('a', {'class': 'player-tabs__season_stats'})['href']
                    mmrMenu = r6URL + playerInfoMenus
                    html = requests.get(mmrMenu).text
                    bs = BeautifulSoup(html, 'html.parser')

                    # recent season rank box
                    # Rank show in purpose : America - Europe - Asia. This code only support Asia server's MMR
                    getElements = bs.find('div', {
                        'class': 'card__content'})  # first elements with class 'card__contet is latest season content box

                    for ckAsia in getElements.findAll('div', {'class': 'season-stat--region'}):
                        checkRegion = ckAsia.find('div', {'class': 'season-stat--region-title'}).text
                        if checkRegion == "Asia":
                            getElements = ckAsia
                            break
                        else:
                            pass
                    # Player's Tier Information
                    latestSeasonTier = getElements.find('img')['alt']
                    # MMR Datas Info -> [Win,Losses,Abandon,Max,W/L,MMR]
                    mmrDatas = []
                    for dt in getElements.findAll('span', {'class': 'season-stat--region-stats__stat'}):
                        mmrDatas.append(dt.text)

                    embed = discord.Embed(title="r6stats에서 Rainbow Six Siege 플레이어 검색", description="",
                                          color=0x5CD1E5)
                    embed.add_field(name="r6stats에서 플레이어 검색", value=searchLink,
                                    inline=False)
                    embed.add_field(name="플레이어의 기본 정보",
                                    value="Ranking : #" + latestSeasonRanking + " | " + "Level : " + playerLevel,
                                    inline=False)
                    embed.add_field(name="최신 시즌 정보 | Operation : " + OperationName,
                                    value=
                                    "Tier(Asia) : " + latestSeasonTier + " | W/L : " + mmrDatas[0] + "/" + mmrDatas[
                                        1] + " | " + "MMR(Asia) : " + mmrDatas[-1],
                                    inline=False)

                    embed.add_field(name="총플레이시간", value=RankStats[0], inline=True)
                    embed.add_field(name="경기한수", value=RankStats[1], inline=True)
                    embed.add_field(name="경기당 처치", value=RankStats[2], inline=True)
                    embed.add_field(name="총킬", value=RankStats[3], inline=True)
                    embed.add_field(name="총사망", value=RankStats[4], inline=True)
                    embed.add_field(name="K/D 비율", value=RankStats[5], inline=True)
                    embed.add_field(name="우승", value=RankStats[6], inline=True)
                    embed.add_field(name="패배", value=RankStats[7], inline=True)
                    embed.add_field(name="W/L 비율", value=RankStats[8], inline=True)
                    embed.set_thumbnail(url=r6URL + r6Profile)
                    await ctx.send("Player " + playerNickname + "'s stats search", embed=embed)

   

def setup(client):
    client.add_cog(크롤링(client))