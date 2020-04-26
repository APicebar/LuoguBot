from nonebot import on_command, CommandSession
import  requests
import re

month=['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
days=[0,31,28,31,30,31,30,31,31,30,31,30,31]

name=[]
start=[]
length=[]

def get_contest():
    global name,start,length
    name.clear()
    start.clear()
    length.clear()
    url = 'https://codeforc.es/contests'
    res = requests.get(url)
    string = res.text
    name=re.findall('<tr data-contestId="[0-9][0-9][0-9][0-9]">\n<td>\n(.*?)\n</td>',string)
    pattern=re.findall('<span class="format-time" data-locale="en">(.*?)</span>\n</a>\n</td>\n<td>\n(.*?)\n</td>',string)
    for k in pattern:
        string=k[0]
        h=int(string[12]+string[13])+5
        d=int(string[4]+string[5])
        y=int(string[7]+string[8]+string[9]+string[10])
        mi=int(string[15]+string[16])
        mon=string[0]+string[1]+string[2]
        m=0
        for i in range(1,13):
            if mon==month[i]:
                m=i
                break
        if h>23:
            h=h-24
            d=d+1
        if y%4==0:
            days[2]=29
        if d>days[m]:
            d=d-days[m]
            m=m+1
        if m>12:
            m=m-12
            y=y+1
        string=month[m]+'/'
        if d<10:
            string=string+'0'+str(d)+'/'
        else:
            string=string+str(d)+'/'
        string=string+str(y)+' '
        if h<10:
            string=string+'0'+str(h)+':'
        else:
            string=string+str(h)+':'
        if mi<10:
            string=string+'0'+str(mi)
        else:
            string=string+str(mi)
        start.append(string)
        string=k[1]
        length.append(string)
    return res

def AT_get_contest():
    global name,start,length
    name.clear()
    start.clear()
    length.clear()
    url = 'https://atcoder.jp/'
    res = requests.get(url)
    string = res.text
    pattern=re.findall('<div id="contest-table-upcoming">(.*?)<div id="contest-table-recent">',string,re.S)
    # print(pattern[0])
    string=pattern[0]
    test=re.findall('<time class=\'fixtime fixtime-short\'>(.*?)\+0900</time>',string)
    pattern=re.findall('<a href=\'/contests/(.*?)\'>(.*?)</a>',string)
    for i in pattern:
        url = 'https://atcoder.jp/contests/'+i[0]
        res = requests.get(url)
        string = res.text
        orz=re.findall('\(local time\)\n\t\t\t\t\((.*?)\)',string)
        length.append(orz[0])
        name.append(i[1])
    for i in test:
        h=int(i[11]+i[12])
        h=h-1
        orz=i[0:11]+str(h)+i[13:19]
        start.append(orz)
    return res

@on_command('CF', aliases=('CodeForces','cf','codeforces','Codeforces'))
async def CodeForces_Report(session: CommandSession):
    get_contest()
    string='近期 CodeForces 比赛预告:\n------------------\n'
    leng=len(name)
    if leng==0:
        string=string+'近期无比赛\n'
    else:
        for i in range(0,leng):
            string=string+'比赛名称: '+name[i]+'\n比赛开始时间: '+start[i]+'\n比赛时长: '+length[i]+'\n------------------\n'
    await session.send(string)

@on_command('AT', aliases=('ATCoder','at','atcoder','Atcoder','AtCoder'))
async def ATCoder_Report(session: CommandSession):
    AT_get_contest()
    string='近期 ATCoder 比赛预告:\n------------------\n'
    leng=len(name)
    if leng==0:
        string=string+'近期无比赛\n'
    else:
        for i in range(0,leng):
            string=string+'比赛名称: '+name[i]+'\n比赛开始时间: '+start[i]+'\n比赛时长: '+length[i]+'\n------------------\n'
    await session.send(string)