from fastapi import params

from util.database import get_db
from util.logger import Logger
from sqlalchemy import text

logger = Logger().get_logger(__name__)

# 게시판에 관련된 기능
def list(session):
    login_id = session.get('loginId','')
    logger.info(f'login id:{login_id}')
    db = None
    list = []

    if login_id == '':
        return {'list':list,'login':login_id}

    sql = text('''SELECT idx,subject,user_name,reg_date,b_hit 
                    FROM bbs ORDER BY idx DESC;''')

    try :
        db = get_db()
        list = db.execute(sql).mappings().fetchall()
        logger.info(f'list = {list}')
    except Exception as e :
        logger.error(e)
    finally:
        db.close()
        return {'list':list,'login':login_id}

def write(subject, user_name, content, files):
    result = {'success':'false'}
    # bbs 에 subject, user_name, content 저장
    sql = text('insert into bbs (subject,user_name,content)values(:subject,:user_name,:content)')
    params = {'subject':subject, 'user_name':user_name, 'content':content}
    conn = get_db()
    try:
         exec_result = conn.execute(sql, params)
         # exec_result.rowcount = 영향받은 데이터 수
         # logger.info(f'exec_result = {exec_result.rowcount}')
         # exec_result.lastrowid = 가장 마지막 row rkqt
         logger.info(f'exec_result:{exec_result.lastrowid}')
         if exec_result.rowcount > 0:
             result['success'] = 'true'
             conn.commit()
    except Exception as e:
        logger.error(e)
        conn.rollback()
    finally:
        conn.close()
        return result
