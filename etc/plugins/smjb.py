import nonebot

@nonebot.on_command('wuwu', only_to_me=False)
async def wuwu(session: nonebot.CommandSession):
    await session.send("呜呜[CQ:face,id=107]")

@nonebot.on_command('smjb', only_to_me=False)
async def help(session: nonebot.CommandSession):
    await session.send('''LuoguBot --- ???

!wuwu --- 呜呜
''')