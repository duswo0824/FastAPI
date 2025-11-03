from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from logger import Logger

logger = Logger().get_logger(__name__)
logger.info('log 준비 완료')

app = FastAPI()

@app.get('/')
def main():
    return {'msg': 'hello main page'}

# post 방식으로 /login 요청과 id,pw를 받아서 로그에 출력
# cookie 에 받아온 값을 저장

@app.post('/login') # id,pw 노출 X : post
def login(id: str, pw: str,resp: Response):
    # 1. id,pw 받아옴
    logger.info(f'id :{id}/pw : {pw}')
    # 2. 쿠키에 값을 저장(쿠키는 어디에 저장? 고객 PC)
    # 그래서 서버에서 클라이언트로 내려보내기 위해 Response 객체를 활용한다.
    # resp.set_cookie(key,value,max_age)
    resp.set_cookie(key='loginYN', value='OK', max_age=60) # max_age 초단위 3600 : 1시간
    resp.set_cookie(key='user_id', value=id, max_age=60)
    resp.set_cookie(key='user_pw', value=pw, max_age=60)
    return{'msg': '로그인 성공!'} # F12 > Application 에서 보면 저장된 내용이 다 나옴

@app.get('/read')
def read_cookie(req: Request):
    dict = req.cookies # cookie의 값을 dictionary 형태로 반환
    logger.info(f'cookies : {dict}')
    return dict

@app.delete('/remove/{key}')
def del_cookie(key:str,req: Request,resp: Response):
    logger.info(f'지우고 싶은 쿠키의 값 : {key}')
    # 해당되는 key의 쿠키값을 지워보자!
    # 힌트 : 저장을 통해 삭제한다.
    resp.set_cookie(key=key, value='', max_age=0)
    return{'msg':'쿠키의 해당 값 삭제'}


