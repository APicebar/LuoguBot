import nonebot

bot = nonebot.get_bot()

@nonebot.on_command('wuwu', only_to_me=False)
async def wuwu(session: nonebot.CommandSession):
    await session.send("呜呜[CQ:face,id=107]")

@nonebot.on_command('fuck', only_to_me=False, permission=nonebot.permission.GROUP)
async def fuck(session: nonebot.CommandSession):
    await session.send("去他妈的")
    await bot.set_group_ban(group_id=session.event.group_id, user_id=session.event.user_id, duration=10)

@nonebot.on_command('smjb', only_to_me=False)
async def help(session: nonebot.CommandSession):
    await session.send('''LuoguBot --- ???

!wuwu --- 呜呜
!fuck --- 表达愤怒''')