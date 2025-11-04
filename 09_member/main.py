from typing import Annotated, Any, Dict

from fastapi import FastAPI, Body
from starlette.middleware.cors import CORSMiddleware

from logger import Logger

app = FastAPI()
logger = Logger().get_logger(__name__)
logger.info('log 준비완료')

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],allow_methods=['*'],allow_headers=['*']) # 전체 허용

@app.get('/')
def main():
    return {'msg': 'this is main page'}

@app.post('/login')
# def login(id: Annotated[str,Body(embed=True)],pw: Annotated[str,Body(embed=True)]):
#     logger.info(f'id :{id}/pw : {pw}')
#     return {'id': id, 'pw': pw}
def login(info:Annotated[Dict[str,Any],Body()]):
    logger.info(f'info:{info}')
    user_id = info['id']
    user_pw = info['pw']
    msg = '아이디 또는 비밀번호를 확인해 주세요!'
    success = False

    if user_id == 'admin' and user_pw == 'pass':
        msg = '로그인에 성공 하였습니다.'
        success = True

    return {'msg': msg,'success': success}

@app.post('/join')
def join(info:Annotated[Dict[str,Any],Body()]):
    logger.info(f'info:{info}')
    result = {'info':info, 'msg':'회원가입에 성공 하였습니다.'}
    return result
