from nonebot import on_command, CommandSession
import requests
from urllib import request
import urllib
import re

Rating=0
Rank=''
MaxRating=0
MaxRank=''
chk=[]

def get_CF_rating(name):
    global Rating,MaxRating,Rank,MaxRank,chk
    Rating=0
    chk.clear()
    url='https://codeforces.com/api/user.info?handles='+name
    res = requests.get(url)
    string = res.text
    chk=re.findall('"status"\:"(.*?)"',string)
    if chk[0]=='FAILED':
        return
    rating=re.findall('"rating"\:(.*?),',string)
    if len(rating)==0:
        return
    Rating=str(rating[0])
    rating=re.findall('"maxRating"\:(.*?),',string)
    MaxRating=str(rating[0])
    rank=re.findall('"rank"\:"(.*?)"',string)
    Rank=rank[0]
    rank=re.findall('"maxRank"\:"(.*?)"',string)
    MaxRank=rank[0]

def get_AT_rating(name):
    global Rating,MaxRating,Rank,chk
    Rank=''
    url='https://atcoder.jp/users/'+name
    res = requests.get(url)
    string = res.text
    chk=re.findall('<title>(.*?)</title>',string)
    if chk[0]=='404 Not Found - AtCoder':
        return
    rank=re.findall('<th class="no-break">Rank</th><td>(.*?)</td></tr>',string)
    if len(rank)==0:
        return
    Rank=rank[0]
    rating=re.findall('<tr><th class="no-break">Rating</th><td><span class=\'.*?\'>(.*?)</span>',string)
    Rating=rating[0]
    rating=re.findall('\t\t\t\t\t\t<span class=\'.*?\'>(.*?)</span>',string)
    MaxRating=rating[0]

@on_command('cfrating', aliases=('CFrating','CFRating'))
async def cfrating(session: CommandSession):
    name = session.current_arg_text.strip()
    if not name:
        await session.send('你要查谁¿')
        return
    get_CF_rating(name)
    if Rating==0:
        ret=name+'\nRating: UnRated\nRank: UnRated'
    elif chk[0]=='OK':
        ret=name+'\nRating: '+Rating+'\nRank: '+Rank+'\nMaxRating: '+MaxRating+'\nMaxRank: '+MaxRank
    else :
        ret='没这个人!'
    await session.send(ret)

@on_command('atrating', aliases=('ATrating','atRating','ATCrating','atcrating','atcRating'))
async def atrating(session: CommandSession):
    name = session.current_arg_text.strip()
    if not name:
        await session.send('你要查谁¿')
        return
    get_AT_rating(name)
    if len(Rank)!=0:
        ret=name+'\nRating: '+Rating+'\nRank: '+Rank+'\nMaxRating: '+MaxRating
    elif chk[0]=='404 Not Found - AtCoder':
        ret='没这个人!'
    else:
        ret=name+'\nRating: UnRated\nRank: UnRated'
    await session.send(ret)