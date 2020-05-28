import nonebot
import json
import config
import re
from datetime import timedelta

enable_group = json.load(open("./data/enable.json")).get('enable_group', None)
bot = nonebot.get_bot()

@nonebot.on_command('sleep', permission=nonebot.permission.GROUP, only_to_me=False)
async def sleep(session: nonebot.CommandSession):
    if session.event.group_id in enable_group:
        await bot.set_group_ban(group_id=session.event.group_id, user_id=session.event.user_id, duration=21600)
        await session.send("发烟成功: 8小时\n晚安qwq")

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
    if arg['minute'] >= 60 or arg['hour'] >= 24 or arg['day'] >= 30:
        await session.send("没这种格式, 重新输入罢")
        return
    time = timedelta(days=arg['day'], minutes=arg['minute'], hours=arg['hour']).total_seconds()
    reply = "发烟成功: "
    if arg['day']:
        reply += (str(arg['day']) + "天")
    if arg['hour']:
        reply += (str(arg['hour']) + "小时")
    if arg['minute']:
        reply += (str(arg['minute']) + "分")
    await bot.set_group_ban(group_id=session.event.group_id, user_id=session.event.user_id, duration=time)
    await session.send(reply)

@nonebot.on_command('抽烟功能', only_to_me=False)
async def help(session: nonebot.CommandSession):
    await session.send('''LuoguBot --- Smoking

!smoke --- 1小时抽烟, 冷静一下
!sleep --- 8小时精致睡眠套餐
!afk [arg] --- 指定时长发烟
    格式为xdxhxm x为整数
    例: !afk 11d4h51m
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
        session.state['minute'] = 10
        return
    if not striparg.isalnum():
        await session.send("格式不对!")
        nonebot.command.kill_current_session(session.event)
    rem = re.compile(r"((\d)?\d)m").search(striparg).group(1)
    red = re.compile(r"((\d)?\d)d").search(striparg).group(1)
    reh = re.compile(r"((\d)?\d)h").search(striparg).group(1)
    minute = 0
    hour = 0
    day = 0
    if rem:
        minute = int(rem)
    if reh:
        hour = int(reh)
    if red:
        day = int(red)
    session.state['minute'] = minute
    session.state['hour'] = hour
    session.state['day'] = day