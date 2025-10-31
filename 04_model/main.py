from typing import Literal, Annotated

from fastapi import FastAPI,Query
from pydantic import BaseModel, ConfigDict, Field

from logger import Logger
app = FastAPI()
logger = Logger().get_logger(__name__)
logger.info('logger 설정 완료!')

@app.get('/')
def index():
    return {'msg': 'main page'}

class Item(BaseModel): #() 안은 상속
    name: str
    description: str | None = None # str 형태로 들어오거나 안들어온다. 기본값은 None
    price: float
    tax: float | None = None

# post는 body로 데이터를 보내고 get은 url로 보낸다.
# 하지만 post와 get 모두 body 영역은 있다.
# 즉, get 방식으로도 body에 데이터를 실어 보낼 수 있지만 서버에서 받을 준비가 되어있지 않으면 에러발생
# item은 class 형태로 url로 보낼 수 없어 어쩔수 없지 body에 실어 보내고 있다.
# 이것을 url 형태, 즉 Query 형태로 보내고 싶다면??

# @app.post('/insert')
# def insert_item(item: Item):
#     logger.info(f'name: {item.name},price: {item.price}')
#     return item

# Annotated 는 유효성 검사의 목적도 있지만 class 를 원하는 방식대로 가져오는 역할도 수행한다.
@app.get('/insert')
def insert_item(item: Annotated[Item,Query()]):
    logger.info(f'name: {item.name},price: {item.price}')
    return item

class FilterParam(BaseModel):
    model_config = ConfigDict(extra='forbid') # 여기서 설정한 외의 필드가 들어오면 유효성 에러 발생
    limit:int = Field(default=100,gt=0,lt=100) # Field 는 Query 처럼 입력값을 제한할 수 있다.
    offset:int = Field(default=0,ge=0,le=100) # (Post, Put 등에서 사용가능)
    order_by:Literal['ASC','DESC'] = 'ASC' # Literal 은 지정된 값 내에서만 선택하도록 제한
    tags:list[str]=[]

# 유효성 검사를 위해서는 Annotated 타입으로 감싸줘야 한다.
@app.get('/items')
def read_items(filter_param: Annotated[FilterParam,Query()]):
    logger.info(f'filter_param: {filter_param}')
    return filter_param