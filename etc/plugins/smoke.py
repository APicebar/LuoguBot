import nonebot
import json

enable_group = json.load(open("./data/enable.json")).get('enable_group', None)
bot = nonebot.get_bot()

@nonebot.on_command('sleep', permission=nonebot.permission.GROUP, only_to_me=False)
async def sleep(session: nonebot.CommandSession):
    if session.event.group_id in enable_group:
        await bot.set_group_ban(group_id=session.event.group_id, user_id=session.event.user_id ,duration=28800)
        await session.send("执行成功: 8小时\n晚安qwq")
    else:await session.send("本群内未启用")

# TODO: Add cancel command.
"""@nonebot.on_command('cancel', permission=nonebot.permission.EVERYBODY)
async def cancel(session: nonebot.CommandSession):
    userid = get(session.args.get('userid', session.event.user_id))
    for i in enable_group:
        await bot.set_group_ban(i, userid, 0)
    await session.send("执行成功")"""

@nonebot.on_command('smoke', permission=nonebot.permission.GROUP, only_to_me=False)
async def smoke(session: nonebot.CommandSession):
    if session.event.group_id in enable_group:
        await bot.set_group_ban(group_id=session.event.group_id, user_id=session.event.user_id ,duration=3600)
        await session.send("执行成功: 1小时")
    else:await session.send("本群内未启用")