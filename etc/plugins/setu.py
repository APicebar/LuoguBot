import nonebot
import random
from urllib import request, error
import json

Url = 'https://konachan.net/post.json'

@nonebot.on_command('setu',only_to_me=False)
async def setu(session: nonebot.CommandSession):
    while True:
        r = random.randint(0,249359)
        url = Url + '?page=%d&limit=1' % r
        data = json.loads(request.urlopen(url=url).read())
        if data[0]['rating'] == 'e' or data[0]['rating'] == 'q':
            await session.send("图源评级不确定或为r18，再试一次吧 >_<")
            break
        if data:
            await session.send("[CQ:at,qq=%d]\n[CQ:image,file=%s]" % (session.event.user_id, data[0]['jpeg_url']))
            break

# @setu.args_parser
async def _(session: nonebot.CommandSession):
    pass