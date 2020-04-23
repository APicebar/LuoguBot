import os
import json
import mysql.connector
import nonebot
from datetime import datetime
from aiocqhttp.exceptions import Error as CQHttpError
import sqlite3
from urllib import request

bot = nonebot.get_bot()

# SQLite Init
sqlite = sqlite3.connect('userdata.db')
sqlite_cur = sqlite.cursor()
sqlite_cur.execute('''create table if not exists LuoguBindData(
                    UserQQ int primary key not null,
                    uid int not null,
                    username text not null)''')
nonebot.logger.info('SQLite Init Success.')
#End

# MySQL Init
passwd = 'woyongyuanxihuanbinggun'
dbhost = '120.78.155.13'
dbuser = 'ApiceBar'
conn = mysql.connector.connect(host=dbhost, user=dbuser, password=passwd, database='benbenOB')
cur = conn.cursor()
nonebot.logger.info('MySQL Init Success.')
# End

# Command Zone
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

# @nonebot.scheduler.scheduled_job('cron', day='*', hour=23, minute=59, second=58)
@nonebot.on_command('dk', permission=nonebot.permission.PRIVATE)
async def DailyKingReport():
    date = datetime.now().strftime('%Y-%m-%d')
    cur.execute('''select username,
            count(*) from benben
            where time like %s
            group by uid
            order by count(*) desc
            limit 1''', (date + '%',))
    data = cur.fetchall()
    await bot.send_group_msg(group_id, message='Today\'s Dragonking: ' + data[0][0] +'\nTotal: ' + str(data[0][1]))

@nonebot.on_command('total', permission=nonebot.permission.PRIVATE)
async def GetTotal(session: nonebot.CommandSession):
    date = datetime.now().strftime('%Y-%m-%d')
    cur.execute('''select count(*)
                from benben
                where time like %s''',(date + '%',))
    data = cur.fetchall()
    await session.send('Today\'s total benben: ' + str(data[0][0]))

@nonebot.on_command('bind', permission=nonebot.permission.PRIVATE)
async def bind(session: nonebot.CommandSession):
    userid = session.event.user_id
    uid = session.get('uid', prompt='Usage: /bind <uid>')
    urlconn = request.urlopen('https://www.luogu.com.cn/user/' + uid + '?_contentOnly=1')
    data = urlconn.read();
    rawdict = json.loads(data)
    userdict = rawdict['currentData']['user']
    sqlite_cur.execute('''insert into LuoguBindData (UserQQ, uid ,username) VALUES (?, ?, ?)''', (userid, uid, userdict['name']))
    level = ''
    if userdict['ccfLevel'] == 0:
        level = 'None/Hidden'
    else:
        level = str(userdict['ccfLevel'])
    await session.send('Bind Succeed.\nName: ' + userdict['name'] + '\nACs: ' + str(userdict['passedProblemCount']) + '\nCCFLevel: ' + level)

# Args Parser Zone

@bind.args_parser
async def _(session: nonebot.CommandSession):
    striparg = session.current_arg_text.strip()
    if session.is_first_run:
        if striparg:
            session.state['uid'] = striparg
            return 
    if not striparg:
        session.pause('No uid input.\nUsage: /bind <uid>')
    session.state[session.current_key] = striparg
