import nonebot
import json
import config

enable_group = json.load(open("./data/enable.json")).get('enable_group', None)
bot = nonebot.get_bot()

@nonebot.on_command('sleep', permission=nonebot.permission.GROUP, only_to_me=False)
async def sleep(session: nonebot.CommandSession):
    if session.event.group_id in enable_group:
        await bot.set_group_ban(group_id=session.event.group_id, user_id=session.event.user_id, duration=28800)
        await session.send("执行成功: 8小时\n晚安qwq")

# TODO: Add cancel command.
@nonebot.on_command('cancel', only_to_me=False)
async def cancel(session: nonebot.CommandSession):
    userid = session.args.get('userid', session.event.user_id)
    if userid != session.event.user_id:
        if session.event.user_id not in config.SUPERUSERS:
            await session.send("执行失败，你谁?")
            return
    for i in enable_group:
        await bot.set_group_ban(group_id=i, user_id=userid, duration=0)
    await session.send("执行成功")

@nonebot.on_command('smoke', permission=nonebot.permission.GROUP, only_to_me=False)
async def smoke(session: nonebot.CommandSession):
    if session.event.group_id in enable_group:
        await bot.set_group_ban(group_id=session.event.group_id, user_id=session.event.user_id ,duration=3600)
        await session.send("执行成功: 1小时")

@nonebot.on_command('抽烟功能', only_to_me=False)
async def help(session: nonebot.CommandSession):
    await session.send('''LuoguBot --- Smoking

!smoke --- 1小时抽烟, 冷静一下
!sleep --- 8小时精致睡眠套餐
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