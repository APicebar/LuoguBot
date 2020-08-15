import nonebot
import json
import config
import re
from datetime import timedelta

enable_group = json.load(open("./data/config.json")).get('enable_group', None)
banlist = json.load(open("./data/config.json")).get('banlist', None)
bot = nonebot.get_bot()

@nonebot.on_command('sleep', permission=nonebot.permission.GROUP, only_to_me=False)
async def sleep(session: nonebot.CommandSession):
    if session.event.group_id in enable_group:
        await bot.set_group_ban(group_id=session.event.group_id, user_id=session.event.user_id, duration=21600)
        await session.send("发烟成功: 6小时\n晚安qwq")

@nonebot.on_command('cancel', only_to_me=False)
async def cancel(session: nonebot.CommandSession):
    userid = session.args.get('userid', session.event.user_id)
    if userid != session.event.user_id:
        if session.event.user_id not in config.SUPERUSERS:
            await session.send("灭烟失败，你谁?")
            return
    for i in enable_group:
        await bot.set_group_ban(group_id=i, user_id=userid, duration=0)
    await session.send("灭烟成功")

@nonebot.on_command('smoke', permission=nonebot.permission.GROUP, only_to_me=False)
async def smoke(session: nonebot.CommandSession):
    if session.event.group_id in enable_group:
        await bot.set_group_ban(group_id=session.event.group_id, user_id=session.event.user_id, duration=3600)
        await session.send("发烟成功: 1小时")

@nonebot.on_command('afk', permission=nonebot.permission.GROUP, only_to_me=False)
async def afk(session: nonebot.CommandSession):
    arg = session.args
    try:
        if arg['4'] >= 60 or arg['3'] >= 60 or arg['2'] >= 24 or arg['1'] > 30:
            await session.send("没这种格式, 重新输入罢")
            return
    except KeyError:
        return
    time = timedelta(days=arg['1'], minutes=arg['3'], hours=arg['2'], seconds=arg['4']).total_seconds()
    if time == 0:
        await session.send("0s禁言你horse呢?")
        return
    if time > 2592000:
        await session.send("超过30天力!")
        return
    reply = "发烟成功: "
    if arg['1']:
        reply += (str(arg['1']) + "天")
    if arg['2']:
        reply += (str(arg['2']) + "小时")
    if arg['3']:
        reply += (str(arg['3']) + "分")
    if arg['4']:
        reply += (str(arg['4']) + "秒")
    await bot.set_group_ban(group_id=session.event.group_id, user_id=session.event.user_id, duration=int(time))
    await session.send(reply)

# '1': day, '2': hour, '3': minute, '4': second

@nonebot.on_command('抽烟功能', only_to_me=False)
async def help(session: nonebot.CommandSession):
    await session.send('''LuoguBot --- Smoking

!smoke --- 1小时抽烟, 冷静一下
!sleep --- 8小时精致睡眠套餐
!afk [arg] --- 指定时长发烟
    格式为xdxhxmxs x为整数
    例: !afk 11d4h51m4s
!cancel [QQ号] --- 取消禁言

cancel时如果指定QQ号则需要超级用户权限''')

@cancel.args_parser
async def _(session: nonebot.CommandSession):
    striparg = session.current_arg.strip()
    if striparg:
        if striparg.isdigit():
            session.state['userid'] = striparg
        else:
            await session.send("这是qq号¿")
            nonebot.command.kill_current_session(session.event)

@afk.args_parser
async def __(session: nonebot.CommandSession):
    striparg = session.current_arg.strip()
    if not striparg:
        session.state['3'] = 10
        return
    if not striparg.isalnum():
        await session.send("格式不对!")
        return
    reg = re.compile(r"((\d+)d)?((\d+)h)?((\d+)m)?((\d+)s)?").search(striparg)
    for i in range(2, 9, 2):
        if reg.group(i):
            session.state['%d' % (i/2)] = int(reg.group(i))
        else:
            session.state['%d' % (i/2)] = 0
