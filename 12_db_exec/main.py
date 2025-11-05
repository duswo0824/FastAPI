# pip install pymysql sqlalchemy
from fastapi import FastAPI

from database import get_db
from logger import Logger
from sqlalchemy import text

app = FastAPI()
logger = Logger().get_logger(__name__)

@app.get("/")
def root():
    db = get_db()
    logger.info(f"DB info: {db}")
    msg = 'DB 접속에 실패 했습니다.' # 기본값

    if db is not None:
        msg = 'DB 접속에 성공 했습니다.'
        db.close()
    return {"msg": msg}

@app.get("/list")
def emp_list():
    db = None
    result = None
    try:
        db = get_db()  # 1. DB 가져오기(session)
        sql = "select * from employees"  # 2. 쿼리문 준비
        # 3. 쿼리문 실행(select) -> # 4. 실행 결과 가져오기(mappings() 를 사용해서 가져옴)
        result = db.execute(text(sql)).mappings().fetchall()  # fetchall 은 여러개를 가져올 때
    except Exception as e: # 만약에 error 가 났을 때
        logger.info(f'error: {e}') # error 값 보여주기
        result = []
    finally:
        db.close() # 5. 사용한 세션 닫아주기
        return {"result": result}

@app.get("/detail/{emp_no}")
def emp_detail(emp_no: str):
    db = None
    result = None
    try:
        db = get_db() # 1. DB 가져오기 (세션접속)
        spl = text('select * from employees where emp_no = :no') # 2. 쿼리문 준비
        # 3. 쿼리문 실행(쿼리문, 파라메터 내용) -> # 4. 결과값 가져오기_ fetchone() 결과값 하나
        result = db.execute(spl,{'no':emp_no}).mappings().fetchone()
    except Exception as e:
        logger.info(f'error: {e}')
        result = {}
    finally:
        # 5. 닫아주기 (자원반납)
        db.close()
        return {"result": result}

@app.get("/insert") # get 방식 : /insert?name=na
def insert(name:str):
    db = None
    row = 0
    try:
        db = get_db()
        spl = text('insert into auto_inc(name) values(:name)')
        # select 를 제외하고는 mappings() 와 fetch 가 필요없다.
        result = db.execute(spl, {'name': name})
        logger.info(f'result: {result.rowcount}') # rowcount 는 DB에서 updated row 이다.
        row = result.rowcount
        db.commit() # autocommit = false 이므로 직접 commit 처리
    except Exception as e:
        logger.info(f'error: {e}')
        row = -1
        db.rollback()
    finally:
        db.close()
        return {"row": row}
