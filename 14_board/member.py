# 회원에 관련된 기능
from typing import Dict
from util.logger import Logger
from sqlalchemy import text
from util.database import get_db

logger = Logger().get_logger(__name__)

def login(info: Dict[str, str], session):
    logger.info(info)
    success = 0  # 기본값을 실패 잡음 (1이 성공)
    db = None
    sql = text('SELECT COUNT(id) AS cnt FROM member WHERE id = :id AND pw = :pw')

    try:
        db = get_db()
        result = db.execute(sql, info).mappings().fetchone()
        logger.info(f'result = {result}')
        success = result['cnt']
        if success >0 :
            session['loginId'] = info['id']
            logger.info(f'loginId = {session["loginId"]}')

    except Exception as e:
        logger.error(e)
    finally:
        db.close()
        return success
