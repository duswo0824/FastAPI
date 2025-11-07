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
