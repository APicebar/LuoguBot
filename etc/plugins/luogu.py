import json
import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
import sqlite3
import random
from urllib import request, error
import hashlib
import re

# SQLite Init
sqlite = sqlite3.connect('./data/luogu/data.db')
sqlite_cur = sqlite.cursor()
sqlite_cur.execute('''create table if not exists LuoguBindData(
                    UserQQ int primary key not null,
                    uid int not null,
                    username text not null,
                    rp int not null)''')
nonebot.logger.info('SQLite Init Success.')
# End

# Luogu & config Init
rawdata = json.load(open("./data/luogu/config.json"))
url = "https://www.luogu.com.cn"
salt = rawdata['salt']
header = {}
header['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"
header['Cookie'] = rawdata['cookie']
# End

# Other
bot = nonebot.get_bot()
scr = re.compile(r'(\d)+')
status = {3:'OLE', 12:'AC', 6:'WA', 5:'TLE', 4:'MLE', 11:'UKE', 7:'RE'}
# End

def get_rec(uid, session: nonebot.CommandSession):
    req = request.Request(headers=header,url=url+"/record/list?_contentOnly&user="+str(uid))
    try:
        data = json.loads(request.urlopen(req).read())
    except error.HTTPError:
        # await session.send("你咕炸力，连不上!")
        return 502
    try:
        rec = data['currentData']['records']['result']
        if not rec:
            # await session.send("没有记录啊.jpg")
            return 404
        rec = rec[0]
    except KeyError:
        # await session.send("拿到的数据不对，是不是cookie被下了?\n已经report给鸽棍了，等着修吧")
        # await bot.send_private_msg(user_id=912370623, message="cookie好像被下了，去检修罢")
        return -1
    try:
        req = request.Request(url=url+"/record/"+str(rec['id'])+"?_contentOnly", headers=header)
        data = json.loads(request.urlopen(req).read())
    except error.HTTPError:
        return 502
    return data['currentData']['record']

def build_msg(rec: dict):
    msg = rec['user']['name'] + ' ' + rec['problem']['pid']
    if rec['status'] == 12: msg += ('\nAC %d' % rec['score'])
    else: msg += ('\nUnAC %d' % rec['score'])
    msg += (' | %dKB | %dms' % (rec['memory'], rec['time']))
    return msg

@nonebot.on_command('stat', only_to_me=False)
async def stat(session: nonebot.CommandSession):
    try: uid = session.args['uid']
    except KeyError: 
        return
    if int(uid) == 117697:
        await session.send("你查这个傻逼干啥")
        return
    try:
        urlconn = request.urlopen('https://www.luogu.com.cn/user/' + uid + '?_contentOnly=1')
    except error.HTTPError:
        await session.send("你咕炸力，连不上!")
        return
    data = urlconn.read()
    rawdict = json.loads(data)
    if rawdict['code'] == 404:
        await session.send('没这个人!')
        return
    userdict = rawdict['currentData']['user']
    level = ''
    if userdict['ccfLevel'] == 0:
        level = '无/藏了以方便假'
    else:
        level = str(userdict['ccfLevel'])
    await session.send(userdict['name'] + '\n关注: ' + str(userdict['followingCount']) \
            + '\n粉丝: ' + str(userdict['followerCount']) + '\nACs/Submits: ' +str(userdict['passedProblemCount']) \
            + '/' + str(userdict['submittedProblemCount']) + '\n颜色: ' + userdict['color'] \
            + '\nCCF评级:' + level)


@nonebot.on_command('bind', permission=nonebot.permission.PRIVATE)
async def bind(session: nonebot.CommandSession):
    args = session.args
    try:
        req = request.urlopen(url + "/user/" + args['uid'] + '?_contentOnly')
    except KeyError: pass
    except error.HTTPError:
        await session.send("你咕炸力，连不上!")
        return
    raw = json.loads(req.read())
    if raw['code'] == 404:
        await session.send("没这个人!")
        return
    data = raw['currentData']['user']
    if data['slogan'] == args['check'] :
        sqlite_cur.execute("insert into LuoguBindData values(%d, %d, '%s', 100)" % 
                            (session.event.user_id, data['uid'], data['name']))
        sqlite.commit()
        await session.send("绑定成功!\n%s\nAC/Submit: %d/%d\nCCF评级: %d" % 
                    (data['name'], data['passedProblemCount'], data['submittedProblemCount'], data['ccfLevel']))
    else:
        await session.send("绑定失败，匹配不成功")

@nonebot.on_command('recent', only_to_me=False)
async def recent(session: nonebot.CommandSession):
    sqlite_cur.execute('select uid from LuoguBindData where UserQQ = ?', (session.event.user_id, ))
    data = sqlite_cur.fetchall()
    if not data:
        await session.send("你还没绑定呢.jpg")
        return
    rec = get_rec(data[0][0], session)
    if rec == 502:
        await session.send("你咕炸力，连不上!")
        return
    elif rec == 404:
        await session.send("没有记录啊.jpg")
        return
    elif rec == -1:
        await session.send("拿到的数据不对，是不是cookie被下了?\n已经report了，等着修吧")
        await bot.send_private_msg(user_id=912370623, message="cookie好像被下了，去检修罢")
        return
    else: pass
    msg = build_msg(rec)
    await session.send(msg)
    

@nonebot.on_command('help', only_to_me=False)
async def help(session: nonebot.CommandSession):
    await session.send('''LuoguBot Beta

!bind <uid> --- 绑定洛谷账号
!stat [uid] --- 查询洛谷
!外网功能
!抽烟功能
!smjb

by APicebar & Naive_Cat''')

@bind.args_parser
async def _(session: nonebot.CommandSession):
    if session.is_first_run:
        striparg = session.current_arg.strip()
        if not striparg:
            await session.send("uid呢?\n!bind <uid>")
            return
        uid = scr.search(striparg).group()
        if not uid:
            await session.send("这8是uid\n!bind <uid>")
            return
        req = request.urlopen(url + "/user/" + uid + '?_contentOnly')
        raw = json.loads(req.read())
        if raw['code'] == 404:
            await session.send("没这个人!")
            return
        session.state['uid'] = uid
        rand = str(random.randint(1,1919810)) + salt + uid
        check = hashlib.md5(rand.encode('utf-8')).hexdigest()
        session.state['check'] = check
        session.pause("请将个人主页的签名改为以下字符:\n\n" + check + "\n\n后回复任意消息验证")

@stat.args_parser
async def __(session: nonebot.CommandSession):
    striparg = session.current_arg_text.strip()
    if striparg:
        if striparg.isdigit():
            session.state['uid'] = striparg
            return
        else:
            await session.send("这是uid¿")
            return
    if not striparg:
        sqlite_cur.execute('select uid from LuoguBindData where UserQQ = ?', (session.event.user_id, ))
        data = sqlite_cur.fetchall()
        if data:
            session.state['uid'] = str(data[0][0])
        if not data:
            await session.send('没有绑定或者uid!')
            return