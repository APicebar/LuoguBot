import nonebot
import random
from urllib import request, error
import json
from datetime import timedelta, datetime

Url = 'https://konachan.net/post.json'
cd = {}

@nonebot.on_command('setu',only_to_me=False)
async def setu(session: nonebot.CommandSession):
    cd.get(session.event.user_id, datetime(1970, 1, 1, 0, 0, 0))
    t = datetime.now() - cd[session.event.user_id]
    if t.seconds() < 240:
        await session.send("乖, 不能太贪心哦←_←\n剩余%d秒" % t.seconds())
        return
    while True:
        r = random.randint(0,249359)
        url = Url + '?page=%d&limit=1' % r
        data = json.loads(request.urlopen(url=url).read())
        if data[0]['rating'] == 'e' or data[0]['rating'] == 'q':
            await session.send("图源评级不确定或为r18，再试一次吧 >_<")
            break
        if data:
            await session.send("[CQ:at,qq=%d]\n[CQ:image,file=%s]" % (session.event.user_id, data[0]['jpeg_url']))
            cd[session.event.user_id] = datetime.now()
            break

# @setu.args_parser
async def _(session: nonebot.CommandSession):
    pass