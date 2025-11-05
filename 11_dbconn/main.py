# pip install pymysql sqlalchemy
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from logger import Logger

app = FastAPI()
logger = Logger().get_logger(__name__)

url = 'mysql+pymysql://web_user:pass@localhost:3306/mydb'

@app.get("/")
def main():
    return {"msg": "main page"}

@app.get("/db/conn")
def db_conn():
    # 1. DB 엔진 생성
    engine = create_engine(url)
    # 2. 세션 생성(DB를 사용하기 위한 권한)
    session = sessionmaker(bind=engine)

    # 3. DB 접속 - session 객체가 있어야 이걸가지고 뭐라도 할 수 있다.
    db = session()
    logger.info(f'db:{db}') # 접속 확인
    db.close() # 4. DB 사용 후 반드시 닫아줘야 한다.
    return{"msg":"db 접속 완료"}