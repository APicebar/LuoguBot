import nonebot
import random
from urllib import request, error
import json
from datetime import timedelta, datetime

Url = ['http://www.dmoe.cc/random.php?return=json',
    'https://img.paulzzh.tech/touhou/random?proxy=1&size=all&site=all']
cd = {}

@nonebot.on_command('setu',only_to_me=False)
async def setu(session: nonebot.CommandSession):
    cd[session.event.user_id] = cd.get(session.event.user_id, datetime(1970, 1, 1, 0, 0, 0))
    t = datetime.now() - cd[session.event.user_id]
    if t.total_seconds() < 240:
        await session.send("乖, 不能太贪心哦←_←\n剩余%d秒" % (240 - int(t.total_seconds())))
        return
    site = random.randint(0,1)
    if site == 0:
        data = json.loads(request.urlopen(url=Url[site]).read())
        await session.send("[CQ:image,file=%s]" % data['imgurl'])
        cd[session.event.user_id] = datetime.now()
    else:
        await session.send("[CQ:image,file=%s]" % Url[site])
        cd[session.event.user_id] = datetime.now()

# @setu.args_parser
async def _(session: nonebot.CommandSession):
    pass