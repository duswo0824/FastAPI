from fastapi import FastAPI
from starlette.requests import Request

from logger import Logger

app = FastAPI()
logger = Logger().get_logger(__name__)
logger.info('log 준비 완료!!!')

# header - 일반적으로 client 에서 보내고 server 에서 받는 구조
# client 로 부터 header를 받고 싶다면? Request
@app.get('/')
def main(req: Request):
    header = req.headers
    for key in header.keys():
        logger.info(f'key: {key} value: {header[key]}')
    return {'msg': 'main page'}