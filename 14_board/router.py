# pip install pymysql sqlalchemy
# pip install itsdangerous
from typing import Dict

# Router 는 본래 분배하는 역할 수행
# client 로 부터 요청이 들어오면 해당 요청을 분배
# 기존 main 에서 처리하던일을 나눠서 처리한다는 개념
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from util.logger import Logger
import member
import board

app = FastAPI()

app.mount("/view", StaticFiles(directory="view"), name="view")
app.mount("/upload", StaticFiles(directory="upload"), name="upload")

# session 사용을 위한 middleware 추가
app.add_middleware(SessionMiddleware, secret_key="session_secret_key", max_age=1800)

logger = Logger().get_logger(__name__)

#uvicorn router:app --reload
@app.get("/")
def main():
    # redirect 는 특정 요청을 호출하는 개념
    # 브라우저 주소창에 주소를 입력한다 생각하자
    return RedirectResponse("/view/login.html")

@app.post("/login")
def login(info: Dict[str, str], req:Request):
    # 요청을 받아서 member 에게 일을 시킴
    session = req.session
    success = member.login(info, session)
    return {"success": success}

@app.get("/list")
def list(req:Request):
    return board.list(req.session)

@app.get("/logout")
def logout(req:Request):
    req.session.clear()
    return RedirectResponse("/view/login.html")