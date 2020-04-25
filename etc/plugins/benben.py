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
sqlite = sqlite3.connect('./data/benben/data.db')
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
def ReConnectDB():
    if cur:
        cur.close()
    else:
        nonebot.logger.info('No cursor, skip')
    if conn:
        conn.close()
    else:
        nonebot.logger.info('No connection, skip')
    conn = mysql.connector.connect(host=dbhost, user=dbuser, password=passwd, database='benbenOB')
    cur = conn.cursor()
    nonebot.logger.info('Database Reconnected.')

# @nonebot.scheduler.scheduled_job('cron', day='*', hour=23, minute=59, second=58)
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
    await session.send('Today\'s DragonKing: ' + data[0][0] + '\nTotal: ' + str(data[0][1]))
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
    try: uid = session.args['uid']
    except KeyError: await session.send('No uid input.\n/bind <uid>')
    urlconn = request.urlopen('https://www.luogu.com.cn/user/' + uid + '?_contentOnly=1')
    data = urlconn.read();
    rawdict = json.loads(data)
    if rawdict['code'] == 404:
        await session.send('Bind Failed: Invalid user.')
        return
    if rawdict['code'] == 502:
        await session.send('Bind Failed: Cannot connect to Luogu.\n(Is Luogu exploded?)')
        return
    userdict = rawdict['currentData']['user']
    try:
        sqlite_cur.execute('''insert into LuoguBindData (UserQQ, uid ,username) VALUES (?, ?, ?)''', (userid, uid, userdict['name']))
        sqlite.commit()
    except sqlite3.IntegrityError:
        await session.send('Bind Falied: Binded.')
        return
    level = ''
    if userdict['ccfLevel'] == 0:
        level = 'None/Hidden'
    else:
        level = str(userdict['ccfLevel'])
    await session.send('Bind Succeed.\nName: ' + userdict['name'] + '\nSubmits/ACs: ' \
            + str(userdict['submittedProblemCount']) + '/' + str(userdict['passedProblemCount']) + '\nCCFLevel: ' + level)

@nonebot.on_command('stat',permission=nonebot.permission.PRIVATE)
async def stat(session: nonebot.CommandSession):
    try: uid = session.args['uid']
    except KeyError: 
        await session.send('No uid input or binding.')
        return
    urlconn = request.urlopen('https://www.luogu.com.cn/user/' + uid + '?_contentOnly=1')
    data = urlconn.read()
    rawdict = json.loads(data)
    if rawdict['code'] == 404:
        await session.send('Request Failed: Invalid user.')
        return
    if rawdict['code'] == 502:
        await session.send('Request Failed: Cannot connect to Luogu.\n(Is Luogu exploded?)')
        return
    userdict = rawdict['currentData']['user']
    level = ''
    if userdict['ccfLevel'] == 0:
        level = 'None/Hidden'
    else:
        level = str(userdict['ccfLevel'])
    await session.send(userdict['name'] + '\nFollowings: ' + str(userdict['followingCount']) \
            + '\nFollowers: ' + str(userdict['followerCount']) + '\nSubmits/ACs: ' +str(userdict['submittedProblemCount']) \
            + '/' + str(userdict['passedProblemCount']) + '\nNameColor: ' + userdict['color'] \
            + '\nCCFLevel:' + level)

@nonebot.on_command('unbind', permission=nonebot.permission.PRIVATE)
async def unbind(session: nonebot.CommandSession):
    sqlite_cur.execute('select * from LuoguBindData where UserQQ = ?', (session.event.user_id, ))
    if not sqlite_cur.fetchall():
        await session.send('No binding data for you.')
        return
    sqlite_cur.execute('delete from LuoguBindData where UserQQ = ?', (session.event.user_id, ))
    sqlite.commit()
    await session.send('Unbind Succeed.')

@nonebot.on_command('help', permission=nonebot.permission.PRIVATE)
async def help(session: nonebot.CommandSession):
    await session.send('''LuoguBot Beta

/dk --- Today\'s DragonKing
/total --- Today\'s total benben
/bind <uid> --- Bind your Luogu account
/stat [uid] --- Status for Luogu
/unbind --- Unbind your Luogu account

by APicebar & Naive_Cat''')
    
# Args Parser Zone

@bind.args_parser
async def _(session: nonebot.CommandSession):
    striparg = session.current_arg_text.strip()
    if striparg:
        session.state['uid'] = striparg
        return 
    if not striparg:
        return

@stat.args_parser
async def __(session: nonebot.CommandSession):
    striparg = session.current_arg_text.strip()
    if striparg:
        session.state['uid'] = striparg
        return
    if not striparg:
        sqlite_cur.execute('select uid from LuoguBindData where UserQQ = ?', (session.event.user_id, ))
        data = sqlite_cur.fetchall()
        if data:
            session.state['uid'] = str(data[0][0])
        if not data:
            return
