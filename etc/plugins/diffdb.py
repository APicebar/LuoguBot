import urllib
import nonebot
import sqlite3 as sqlite
from datetime import datetime
from urllib import request, error
import json

db = sqlite.connect("./data/luogu/diffdb.db")
b = sqlite.connect("./data/luogu/data.db")
cur = db.cursor()
bind = b.cursor()
cur.execute('''create table if not exists DiffData(
                    pid text primary key not null,
                    diff int not null)''')
cur.execute('''create table if not exists ChangeRec(
                    id int primary key not null,
                    uid int not null, qq int not null,
                    pid text not null, diff int not null,
                    time text not null)''')
cnt = cur.execute('select count(*) from ChangeRec').fetchall()
cnt = cnt[0][0]

async def insert(pid, diff, uid, qq):
    global cnt
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("insert into DiffData values('%s', %d)" % (pid, diff))
    cur.execute("insert into ChangeRec values(%d, %d, %d, '%s', %d, '%s')" % (cnt, uid, qq, pid, diff, time))
    db.commit()
    cnt += 1

@nonebot.on_command("submit", only_to_me=False)
async def submit(session: nonebot.CommandSession):
    qq = session.event.user_id
    args = session.args
    if args['ok'] == 0: return
    uid = bind.execute("select * from LuoguBindData where UserQQ = %d" % qq).fetchall()
    if not uid:
        await session.send("你还没绑定呢.jpg")
        return
    uid = uid[0][1]
    if cur.execute("select * from DiffData where pid = '%s'" % args['pid']).fetchall():
        await session.send("当前题目已有数据（")
        return
    await insert(args['pid'], args['diff'], uid, qq)
    await session.send("提交成功!")

@nonebot.on_command("难度数据", only_to_me=False)
async def help(session: nonebot.CommandSession):
    await session.send('''LuoguBot --- DiffDatabase Alpha
!submit <pid> <难度系数>
    
难度系数处于[200,3500]间
pid务必带上前缀，如CF1428B, P1577等
不支持U/T前缀的题目''')

@submit.args_parser
async def _(session: nonebot.CommandSession):
    striparg = session.current_arg_text.strip().split()
    try:
        if int(striparg[1]) > 3500 or int(striparg[1]) < 200:
            await session.send("难度定值应在[200,3500]之间")
            session.state['ok'] = 0
            return
        session.state['diff'] = int(striparg[1])
        if striparg[0].startswith("T") or striparg[0].startswith("U"):
            await session.send("不支持U/T前缀的题目 = =")
            session.state['ok'] = 0
            return
        req = request.urlopen("https://www.luogu.com.cn/problem/%s?_contentOnly" % striparg[0]).read()
        data = json.loads(req)
        if data['code'] == 404:
            await session.send("莫得这题，你题号写错了?")
            session.state['ok'] = 0
            return
        session.state['pid'] = striparg[0]
        session.state['ok'] = 1
    except error.HTTPError:
        await session.send("你咕炸力，连不上!")
        session.state['ok'] = 0
        return
    except IndexError:
        await session.send("参数不全（")
        session.state['ok'] = 0
    except ValueError:
        await session.send("非法参数.jpg")
        session.state['ok'] = 0