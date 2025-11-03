from typing import Annotated, Dict, Any

from fastapi import FastAPI, Body
from starlette.middleware.cors import CORSMiddleware

from logger import Logger

app = FastAPI()
logger = Logger().get_logger(__name__)
logger.info('log 준비완료')

# CORS policy
# Cross Origin Resource Sharing - 서로 다른 서버에서 자원을 공유하는 것을 금지
# 이 경우 CORS policy 로 인해 통신이 불가능 하다.\
# 특정한 경우 이 정책을 풀어줄 수 있다.
# Cross Origin
# middle ware - 서버에 도달하기 전 먼저 요청을 가로채서 동작을 수행하는 함수(인터셉터)
app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],allow_methods=['*'],allow_headers=['*'])

@app.get('/')
def main():
    return {'msg':'this is main page'}

@app.get('/get')
def get_test(msg: str):
    logger.info(f'msg:{msg}')
    return {'msg':f'{msg} 내용 잘 받았습니다.'}

@app.post('/post')
def post_test(msg: Annotated[str,Body(embed=True)]):
    logger.info(f'msg:{msg}')
    return {'msg':f'{msg} 내용 잘 받았습니다.'}

# JSON == Dict 형태 (같음)
@app.post('/json')
def json_test(data: Annotated[Dict[str, Any],Body()]):
    logger.info(f'data:{data}')
    data['server'] = '데이터 잘 받았습니다.'
    return data