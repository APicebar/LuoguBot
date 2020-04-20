import mysql.connector
import nonebot
from datetime import datetime
from aiocqhttp.exceptions import Error as CQHttpError

passwd = 'woyongyuanxihuanbinggun'
dbhost = '120.78.155.13'
dbuser = 'ApiceBar'
conn = mysql.connector.connect(host=dbhost, user=dbuser, password=passwd, database='benbenOB')
cur = conn.cursor()

@nonebot.scheduler.scheduled_job('cron', hour='*')
def ConnectDB():
    if cur :
        cur.close()
    else :
        nonebot.logger.info('No cursor, skip')
    if conn :
        conn.close()
    else :
        nonebot.logger.info('No connection, skip')
    conn = mysql.connector.connect(host=dbhost, user=dbuser, password=passwd, database='benbenOB')
    cur = conn.cursor()
    nonebot.logger.info('Database Reconnected.')

# @nonebot.scheduler.scheduled_job('cron', day='*')
@nonebot.on_command('dk', permission=nonebot.permission.PRIVATE)
async def DailyKingReport(session: nonebot.CommandSession):
    date = datetime.now().strftime('%Y-%m-%d')
    cur.execute('''select username,
            count(*) from benben
            where time like %s
            group by uid
            order by count(*) desc
            limit 1''', (date + '%',))
    data = cur.fetchall()
    await session.send('Today\'s Dragonking: ' + data[0][0] +'\nTotal: ' + str(data[0][1]))

@nonebot.on_command('total', permission=nonebot.permission.PRIVATE)
async def GetTotal(session: nonebot.CommandSession):
    date = datetime.now().strftime('%Y-%m-%d')
    cur.execute('''select count(*)
                from benben
                where time like %s''',(date + '%',))
    data = cur.fetchall()
    await session.send('Today\'s total benben: ' + str(data[0][0]))

