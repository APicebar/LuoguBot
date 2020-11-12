import nonebot
import aiocqhttp.exceptions as CQHttpError

bot = nonebot.get_bot()

@nonebot.on_command('feed', only_to_me=False)
async def feed(session: nonebot.CommandSession):
    await session.send("[CQ:image,file=feed.jpg]")

@nonebot.on_command('broadcast', only_to_me=False, permission=nonebot.permission.SUPERUSER)
async def broadcast(session: nonebot.CommandSession):
    try:
        g_list = await bot.get_group_list()
        for i in g_list:
            await bot.send_group_msg(group_id=i['group_id'], message=session.current_arg_text)
    except CQHttpError.ActionFailed:
        await session.send("失败: 账号可能被风控")