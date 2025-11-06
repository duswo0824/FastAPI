# pip install pymysql sqlalchemy
from typing import Annotated, Dict, Any

from fastapi import FastAPI, Body
from starlette.middleware.cors import CORSMiddleware

from database import get_db
from logger import Logger
from sqlalchemy import text

app = FastAPI()
logger = Logger().get_logger(__name__) # 현재 파일명 기준으로 로그 설정
logger.info('log 준비완료') # 서버 시작 시 로그 출력

# CORS 미들웨어
app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],allow_methods=['*'],allow_headers=['*']) # 전체 요청허용

# 기존 URL 접속 확인
@app.get("/")
def root():
    db = get_db() # DB 연결 요청
    logger.info(f"DB info: {db}") # DB 연결 객체 로그 확인
    msg = 'DB 접속에 실패 했습니다.' # 기본값

    if db is not None: # DB 연결 성공 여부 확인
        msg = 'DB 접속에 성공 했습니다.'
        db.close() # 사용한 연결 닫기
    return {"msg": msg} # 결과 반환(JSON) : {}형태

# 로그인
@app.post("/login")
def login(info: Annotated[Dict[str, Any], Body()]):
    db = None
    row = 0
    try:
        db = get_db()
        sql = text("select * from member where id=:id and pw=:pw")
        result = db.execute(sql, info).mappings().fetchone() # 딕셔너리 info에 id, pw 있음
        if result is not None:
            row =1
    except Exception as e:
        logger.info(f'error: {e}')
        row = -1
    finally:
        db.close()
        return {"row": row}


# ID 중복 체크
@app.post("/check_id")
def check_id(info: Annotated[Dict[str, Any], Body()]):
    db = None
    row = 0 # 결과값 → 기본값은 '중복 아님(0)''
    try:
        db = get_db()  # 1. DB 가져오기(세션접속)
        # 2. 쿼리문 준비
        sql = text("select * from member where id=:id")
        # 3. 쿼리문 실행(쿼리문, 파라메터 내용) -> # 4. 결과값 가져오기
        result = db.execute(sql, info).mappings().fetchone()
        if result is not None: # None : id 없음
            row = 1  # 결과가 있으면 중복
    except Exception as e:
        logger.info(f'error: {e}')
    finally:
        db.close()
        return {"row": row}
    
#  회원가입
@app.post("/join")
def join(info:Annotated[Dict[str,Any],Body()]):
    # info = vscode에서 JSON 객체로 넘어온 회원정보
    db = None
    row = 0 # insert 성공 여부를 저장할 변수
    try:
        db = get_db() # 1. DB 가져오기(세션접속)
        # 2. 쿼리문 준비
        sql = text(
            'insert into member(id, pw, name, age, gender, email) values (:id, :pw, :name, :age, :gender, :email)'
        )
        # 3. 쿼리문 실행(쿼리문, 파라메터 내용) -> # 4. 결과값 가져오기
        result = db.execute(sql, info) # info = { id: .., pw: .., name: .., age: .., gender: .., email: .. }
        logger.info(f'result: {result.rowcount}') # result.rowcount : 실제 DB에 반영된 row 수 (updated row=1)
        row = result.rowcount # insert 성공 (회원 1명 추가됨), row = 1
        db.commit()  # autocommit = false 이므로 직접 commit 처리
    except Exception as e: # 만약에 error 가 났을 때
        logger.info(f'error: {e}') # # error 값 보여주기
        row = -1 # insert 실패
        db.rollback() # 에러 발생 / 롤백
    finally:
        db.close() # 5. 사용한 세션 닫아주기
        return {"row": row} # 결과 JSON 반환 (1=성공, -1=실패)

