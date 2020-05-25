import nonebot
import json

enable_group = json.loads(open("./data/enable.json"))
bot = nonebot.get_bot()

@nonebot.on_command('sleep', permission=nonebot.permission.GROUP)
async def sleep(session: nonebot.CommandSession):
    if session.event.group_id in enable_group:
        await bot.set_group_ban(session.event.group_id, session.event.user_id, 28800)
        await session.send("执行成功: 8小时\n晚安qwq")

# TODO: Add cancel command.
"""@nonebot.on_command('cancel', permission=nonebot.permission.EVERYBODY)
async def cancel(session: nonebot.CommandSession):
    userid = get(session.args.get('userid', session.event.user_id))
    for i in enable_group:
        await bot.set_group_ban(i, userid, 0)
    await session.send("执行成功")"""

@nonebot.on_command('smoke', permission=nonebot.permission.GROUP)
async def smoke(session: nonebot.CommandSession):
    if session.event.group_id in enable_group:
        await bot.set_group_ban(session.event.group_id, session.event.user_id, 3600)
        await session.send("执行成功: 1小时")