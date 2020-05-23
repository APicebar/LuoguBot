import pathlib
import json
import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
import sqlite3
import random
from urllib import request
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
# End

# Other
scr = re.compile(r'(\d)+')
# End

@nonebot.on_command('bind', permission=nonebot.permission.PRIVATE)
async def bind(session: nonebot.CommandSession):
    args = session.args
    try:
        req = request.urlopen(url + "/user/" + args['uid'] + '?_contentOnly')
    except KeyError: pass
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

@bind.args_parser
async def _(session: nonebot.CommandSession):
    if session.is_first_run:
        striparg = session.current_arg.strip()
        if not striparg:
            await session.send("uid呢?\n/bind <uid>")
            return
        uid = scr.search(striparg).group()
        if not uid:
            await session.send("这8是uid\n/bind <uid>")
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