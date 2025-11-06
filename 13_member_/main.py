from typing import Dict, Any

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from database import get_db
from logger import Logger
from sqlalchemy import text

app = FastAPI()
logger = Logger().get_logger(__name__)
logger.info('log 준비완료')

# pip install itsdangerous
# session : cookie 처럼 어느 페이지에서나 공유 가능한 저장소
# 서버에 저장되며, 브라우저가 바뀌거나 일정 시간이 지나면 자동 삭제됨
# session 이 얼마나 저장되는지 알고 싶으면 다른 서비스 로그인 후 언제 로그인이 풀리는지 확인해보자
# session 사용시 middleware 에 등록 필요
app.add_middleware(SessionMiddleware, secret_key="session_secret_key")

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
# session 은 request 객체에 있다.
@app.post('/login')
def login(info:Dict[str,Any],req:Request):
    logger.info(f'info={info}')
    sql = text("select count(id) as cnt from member where id = :id and pw = :pw;")
    db = None
    count = 0
    try :
        db = get_db() # DB에 접속
        result = db.execute(sql, info).mappings().fetchone()# id와 pw를 둘다 만족하는 count 확인
        logger.info(f'result={result}')
        count = result['cnt'] # 해당 내용을 count 변수에 대입
        
        if count > 0 :
            req.session['loginId'] = info['id'] # 로그인 했다는 증표로 loginId 라는 이름으로 id 값 저장

    except Exception as e :
        logger.error(e)
    finally:
        db.close()
        return{'success':count} # insert 성공 1

# 회원리스트
@app.get('/list')
def list(req:Request):
    member_list = []
    db = None
    sql = text("select id,name,gender from member;")
    login_id = req.session.get('loginId','') # get(가져올값의 키, 없을 경우 만환할 값)
    logger.info(f'login_id={login_id}')
    if login_id == '': # session에 loginId 값이 없으면...
        return {'list':member_list,'loginId':login_id}

    try:
        db = get_db()
        # 쿼리 실행 후 가져온 내용을 member_list 에 담아서 전송
        member_list = db.execute(sql).mappings().fetchall() # result 자체가 배열[{}]
        logger.info(f'member_list={member_list}')
    except Exception as e :
        logger.error(e)
    finally:
        db.close()
        return {'list':member_list,'loginId':login_id}
