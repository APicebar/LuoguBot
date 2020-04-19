import mysql.connector
import nonebot
from datetime import datetime
from aiocqhttp.exceptions import Error as CQHttpError

"""
def ConnectDB(uid, time):
    passwd='woyongyuanxihuanbinggun'
    conn = mysql.connector.connect(user='ApiceBar', password=passwd, database='benbenOB')
    cur = conn.cursor()
    cur.execute('select count(*) from ')
"""

# @nonebot.scheduler.scheduled_job('cron', day='*')
@nonebot.on_command('dk', permission=nonebot.permission.PRIVATE)
async def DailyKingReport(session: nonebot.CommandSession):
    if session.event.group_id:
        return
    date = datetime.now().strftime('%Y-%m-%d')
    passwd='woyongyuanxihuanbinggun'
    conn = mysql.connector.connect(host='120.78.155.13', user='ApiceBar', password=passwd, database='benbenOB')
    cur = conn.cursor()
    cur.execute('''select username,
            count(*) from benben
            where time like %s
            group by uid
            order by count(*) desc
            limit 1''', (date + '%',))
    data = cur.fetchall()
    cur.close()
    conn.close()
    await session.send('Today\'s Dragonking is ' + data[0][0] +', Total ' + str(data[0][1]))

