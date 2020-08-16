import nonebot

@nonebot.on_command('feed',only_to_me=False)
async def feed(session: nonebot.CommandSession):
    await session.send("[CQ:image,file=feed.jpg]")