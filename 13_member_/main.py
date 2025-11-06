from typing import Dict, Any

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from database import get_db
from logger import Logger
from sqlalchemy import text

app = FastAPI()
logger = Logger().get_logger(__name__)
logger.info('log 준비완료')

# app.add_middleware(CORSMiddleware,)
# html이 py와 같은 서버(경로 view)에 있기 때문에 CORS 정책에서 자유로워졌다.

# /view 라는 요청이 오면 프로젝트내 view 폴더로 연결해라 (/view/login.html 확인 가능)
app.mount("/view",StaticFiles(directory="view"),name="view")

# 아이디 중복확인
@app.get("/overlay")
def overlay(id:str):
    logger.info(f'id={id}')
    db = None
    cnt = 1
    try :
        db = get_db()
        sql = text('select count(id) as cnt from  member where id = :id;')
        result = db.execute(sql,{'id':id}).mappings().fetchone()
        logger.info(f'result={result}')
        cnt = result['cnt']
    except Exception as e :
        logger.error(e)
    finally:
        db.close()
        return {'use':cnt} # 0 이면 사용가능 1 이면 중복

# 회원가입
# 여러 데이터가 올 경우 BaseModel을 상속한 클래스 형태로 받거나(추천)
# 딕셔너리 Dict 형태로 받는다.(편리함)
# 딕셔너리를 사용하면 /docs 에서 볼 때 어떠한 값들이 들어가야 하는지 확인이 안된다.
@app.post('/join')
def join(info:Dict[str,Any]):
    logger.info(f'info={info}')
    db = None
    row = 0
    # """ 는 여러줄 문자열을 인정한다.
    sql = text("""INSERT INTO member(id,pw,name,age,gender,email)
        VALUES(:id,:pw,:name,:age,:gender,:email)""")
    try:
        db = get_db()
        result = db.execute(sql,info)
        logger.info(f'result={result}')
        row = result.rowcount
        db.commit()
    except Exception as e:
        logger.error(e)
        db.rollback()
    finally:
        db.close()
        return {'row':row} # 몇개가 데이터 반환 1 : insert 성공

# 로그인
@app.post('/login')
def login(info:Dict[str,Any]):
    logger.info(f'info={info}')
    sql = text("select count(id) as cnt from member where id = :id and pw = :pw;")
    db = None
    count = 0

    try :
        db = get_db() # DB에 접속
        result = db.execute(sql, info).mappings().fetchone()# id와 pw를 둘다 만족하는 count 확인
        logger.info(f'result={result}')
        count = result['cnt'] # 해당 내용을 count 변수에 대입
    except Exception as e :
        logger.error(e)
    finally:
        db.close()
    return{'success':count} # insert 성공 1
