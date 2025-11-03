from typing import Union

from fastapi import FastAPI, Query, Path

import logging

# level : debug > info > warning > error > critical
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: [%(name)s] %(message)s - %(asctime)s',
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/") # root 최소
def main():
    logger.info('main page connect')
    return {"msg": "메인 페이지 입니다."}

# 요청시 받아야할 파라메터를 가져오지 않으면 서버 입장이 불가능 하다.
# 이 경우를 잘못된 요청(Bad Request 400)이라고 한다.
# 그런데 이 경우 에러가 아닌 기본 값으로 대처할 수 있다.
@app.get("/items/get")
def read_items(skip: int=0, limit: int=10):
    # logger.info('skip : '+str(skip)+' / limit : '+str(limit))
    logger.info(f'skip: {skip}, limit: {limit}')
    return {"skip": skip, "limit": limit}

# union/item1234?q=의류
# q가 들어갈 수도 있고 안들어갈 수도 있는 경우 기본값으로 처리할 수 있다.
# def union_variable(item_id:str, q:str=''):
@app.get("/union/{item_id}")
# 하지만 Union을 활용하면 아예 없는 값으로 처리 할 수도 있다.
# Union은 특정 변수의 형태를 여러가지로 정의해 줄 수 있다.
def union_variable(item_id:str, q:Union[str,None]=None):
    item = {'item_id':item_id}
    if q is not None:
        item.update({'q':q}) # 기존의 dic에 값 추가
    return item

# Query() 는 ? 뒤로 오는 파라메터들(쿼리)에 대해서 기본 값이나 길이 등에 제한을 줄 수 있다.
@app.get("/item")
def read_item(q:Union[str,None]=Query(default=None, max_length=50)):
    result = {'items':[{'item_id':'Foo'},{'item_id':'Bar'}]}
    if q: # is not None
        result.update({'q':q})
    return result

# Path 는 경로 변수를 대상으로 한다.
# /api/num/1234 <- path
#/api?num=1234 <- query
@app.get("/api/path/{item_id}")
def api_path(item_id:int = Path(gt=0),
             q:Union[str,None]=Query(default=None)): # Path(gt=0,lt=1000) <- gt,lt,ge,le

    result = {'items':item_id}

    if q: # is not None
        result.update({'q':q})

    return result
