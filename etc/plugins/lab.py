import nonebot
import re


bot = nonebot.get_bot()

@nonebot.on_command('tag', permission=nonebot.permission.GROUP, only_to_me=False)
async def tag(session: nonebot.CommandSession):
    arg = session.args
    try:
        if arg['qq'] == session.event.user_id:
            await session.send("?不能改自己的")
            return
        await bot.set_group_special_title(group_id=session.event.group_id, user_id=arg['qq'], special_title=arg['str'])
        await session.send("操作成功")
    except KeyError:
        return

@nonebot.on_command("实验室", only_to_me=False, aliases=('lab',))
async def help(session: nonebot.CommandSession):
    await session.send('''LuoguBot --- 实验室

!tag <at> <str> --- 头衔''')

@tag.args_parser
async def _(session: nonebot.CommandSession):
    arg = session.current_arg.strip().split()
    try:
        reg = re.compile(r"CQ:at,qq=(\d+)").search(arg[0])
        nonebot.logger.debug(session.current_arg)
    except IndexError:
        await session.send("给谁?")
        return
    try:
        if reg.group(1):
            session.state['qq'] = int(reg.group(1))
            session.state['str'] = arg[1]
    except IndexError:
        session.state['str'] = ''